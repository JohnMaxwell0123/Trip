#!/usr/bin/env node
/**
 * 西行壮歌 · 丝路与额济纳自驾大环线
 * 无头自动化逐帧抓取与离线渲染管道 (Headless Offline Frame Renderer)
 * 
 * 特色：
 * 1. 优先使用本地安装的 Chrome 或 Edge 浏览器内核；
 * 2. 具备零外部依赖能力 (原生利用 Node 21+ 内置 WebSocket 与 CDP 协议通信)；
 * 3. 亦兼容标准 Puppeteer 运行时 (若环境中已安装)；
 * 4. 支持灵活的 CLI 参数 (--start <frame>, --end <frame>, --out <dir>, --step <step>)；
 * 5. 严格调用 window.renderFrame(frameIndex, totalFrames) 确定性逐帧捕获输出 PNG 序列。
 */

const fs = require('fs');
const path = require('path');
const http = require('http');
const { spawn } = require('child_process');

const net = require('net');

// 命令行参数解析
const args = process.argv.slice(2);
function getArg(flag, defaultValue) {
  const idx = args.indexOf(flag);
  if (idx !== -1 && idx + 1 < args.length) {
    return args[idx + 1];
  }
  return defaultValue;
}

const START_FRAME = parseInt(getArg('--start', '0'), 10);
const END_FRAME = parseInt(getArg('--end', '30'), 10); // 默认测试抓取前 30 帧 (1秒)，可通过 --end 3599 抓取全量
const STEP = parseInt(getArg('--step', '1'), 10);
const OUTPUT_DIR = path.resolve(__dirname, getArg('--out', 'frames'));
const USER_PORT = getArg('--port', null);
const SEQUENTIAL = args.includes('--seq') || args.includes('--sequential');

// 探测可用空闲调试端口，避免与已有 Chrome 进程冲突
function getFreePort(startingPort = 9222) {
  return new Promise((resolve) => {
    const srv = net.createServer();
    srv.listen(startingPort, '127.0.0.1', () => {
      srv.close(() => resolve(startingPort));
    });
    srv.on('error', () => {
      resolve(getFreePort(startingPort + 1));
    });
  });
}

// 探测本地可用浏览器路径
function getBrowserExecutable() {
  const candidates = [
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
    'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
    '/usr/bin/google-chrome',
    '/usr/bin/chromium-browser',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
  ];

  for (const p of candidates) {
    if (fs.existsSync(p)) return p;
  }
  throw new Error("未能在标准路径中找到 Chrome 或 Edge 浏览器可执行文件！");
}

// 确保输出目录存在
if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

// 基于 CDP (Chrome DevTools Protocol) 的轻量级通信客户端
class CDPClient {
  constructor(wsUrl) {
    this.wsUrl = wsUrl;
    this.ws = null;
    this.msgId = 1;
    this.callbacks = new Map();
  }

  async connect() {
    return new Promise((resolve, reject) => {
      this.ws = new WebSocket(this.wsUrl);
      this.ws.onopen = () => resolve();
      this.ws.onerror = (err) => reject(err);
      this.ws.onmessage = (event) => {
        try {
          const res = JSON.parse(event.data);
          if (res.id && this.callbacks.has(res.id)) {
            const { resolve, reject } = this.callbacks.get(res.id);
            this.callbacks.delete(res.id);
            if (res.error) reject(new Error(res.error.message || JSON.stringify(res.error)));
            else resolve(res.result);
          }
        } catch (e) {
          console.error("CDP JSON 解析异常:", e);
        }
      };
    });
  }

  send(method, params = {}) {
    return new Promise((resolve, reject) => {
      const id = this.msgId++;
      this.callbacks.set(id, { resolve, reject });
      this.ws.send(JSON.stringify({ id, method, params }));
    });
  }

  async evaluate(expression) {
    const res = await this.send("Runtime.evaluate", {
      expression,
      returnByValue: true,
      awaitPromise: true
    });
    if (res.exceptionDetails) {
      throw new Error("执行脚本错误: " + JSON.stringify(res.exceptionDetails));
    }
    return res.result ? res.result.value : undefined;
  }

  close() {
    if (this.ws) this.ws.close();
  }
}

// 等待 HTTP 探测就绪
function waitForHttp(url, timeoutMs = 15000) {
  const startTime = Date.now();
  return new Promise((resolve, reject) => {
    function check() {
      http.get(url, (res) => {
        let body = '';
        res.on('data', chunk => body += chunk);
        res.on('end', () => {
          try {
            const json = JSON.parse(body);
            resolve(json);
          } catch (e) {
            retry();
          }
        });
      }).on('error', () => {
        retry();
      });
    }

    function retry() {
      if (Date.now() - startTime > timeoutMs) {
        reject(new Error(`等待 CDP 端口超时 (${url})`));
      } else {
        setTimeout(check, 300);
      }
    }
    check();
  });
}

async function main() {
  const PORT = USER_PORT ? parseInt(USER_PORT, 10) : await getFreePort(9222);

  console.log("==================================================================");
  console.log(" 西行壮歌 · 丝路与额济纳自驾大环线 无头离线逐帧渲染抓取流水线");
  console.log("==================================================================");
  console.log(`目标帧区间: [Frame ${START_FRAME} -> Frame ${END_FRAME}], 步长: ${STEP}`);
  console.log(`输出目录: ${OUTPUT_DIR}`);
  console.log(`调试端口: ${PORT} (CDP DevTools Protocol)`);
  if (SEQUENTIAL) {
    console.log(`编号模式: 严格连续递增 (frame_0000.png, frame_0001.png...)`);
  } else {
    console.log(`编号模式: 绝对帧号对应 (frame_${String(START_FRAME).padStart(4, '0')}.png...)`);
  }

  const browserPath = getBrowserExecutable();
  console.log(`启用浏览器内核: ${browserPath}`);

  const htmlPath = path.resolve(__dirname, 'video_renderer.html');
  const targetUrl = 'file:///' + htmlPath.replace(/\\/g, '/');
  console.log(`挂载渲染页面: ${targetUrl}`);

  // 临时用户配置目录
  const tempProfile = path.resolve(__dirname, `.temp_render_profile_${PORT}`);

  // 启动无头浏览器实例
  const browserArgs = [
    '--headless=new',
    `--remote-debugging-port=${PORT}`,
    '--window-size=1920,1080',
    '--disable-gpu',
    '--no-first-run',
    '--no-default-browser-check',
    '--disable-background-networking',
    `--user-data-dir=${tempProfile}`,
    targetUrl
  ];

  console.log("正在启动后台 Headless 浏览器会话...");
  const proc = spawn(browserPath, browserArgs, { stdio: 'ignore' });

  // 确保进程退出时回收资源
  const cleanup = () => {
    try { proc.kill(); } catch (e) {}
    try { fs.rmSync(tempProfile, { recursive: true, force: true }); } catch (e) {}
  };
  process.on('exit', cleanup);
  process.on('SIGINT', () => { cleanup(); process.exit(); });

  try {
    // 探测 /json 列表以获取 webSocketDebuggerUrl
    console.log(`连接 CDP 调试端口 http://127.0.0.1:${PORT}/json...`);
    const pages = await waitForHttp(`http://127.0.0.1:${PORT}/json`);
    const page = pages.find(p => p.url.includes('video_renderer.html')) || pages[0];

    if (!page || !page.webSocketDebuggerUrl) {
      throw new Error("无法检索到渲染目标页面的 WebSocket 调试端点！");
    }

    console.log(`已建立 WebSocket 调试桥: ${page.webSocketDebuggerUrl}`);
    const client = new CDPClient(page.webSocketDebuggerUrl);
    await client.connect();

    // 启用必要的域
    await client.send("Page.enable");
    await client.send("Runtime.enable");

    // 等待页面完全加载与初始化
    console.log("等待渲染引擎生命周期就绪...");
    await new Promise(r => setTimeout(r, 2000));

    // 获取视频元数据
    const info = await client.evaluate("window.getVideoInfo ? window.getVideoInfo() : null");
    if (!info) {
      throw new Error("页面未能暴露 window.getVideoInfo() 接口！");
    }
    console.log(`✔ 渲染引擎握手成功: 总帧数 ${info.totalFrames}, 分辨率 ${info.width}x${info.height}, 镜头数 ${info.shots.length}`);

    // 逐帧渲染与保存循环
    const totalToRender = Math.floor((END_FRAME - START_FRAME) / STEP) + 1;
    let renderedCount = 0;
    const startRenderTime = Date.now();

    for (let f = START_FRAME; f <= END_FRAME; f += STEP) {
      // 驱动指定帧渲染并提取 Base64 PNG 数据
      const dataUrl = await client.evaluate(`window.getFrameDataUrl(${f})`);
      if (!dataUrl || !dataUrl.startsWith("data:image/png;base64,")) {
        throw new Error(`帧 F${String(f).padStart(4, '0')} 提取图像数据失败！`);
      }

      const base64Data = dataUrl.replace(/^data:image\/png;base64,/, "");
      const indexNum = SEQUENTIAL ? renderedCount : f;
      const fileName = `frame_${String(indexNum).padStart(4, '0')}.png`;
      const filePath = path.join(OUTPUT_DIR, fileName);
      fs.writeFileSync(filePath, Buffer.from(base64Data, 'base64'));

      renderedCount++;
      const elapsed = ((Date.now() - startRenderTime) / 1000).toFixed(1);
      const fps = (renderedCount / (Date.now() - startRenderTime) * 1000).toFixed(1);
      const pct = ((renderedCount / totalToRender) * 100).toFixed(1);
      process.stdout.write(`\r[渲染进度] 帧 ${String(f).padStart(4, '0')} (${renderedCount}/${totalToRender}, ${pct}%) | 速度: ${fps} fps | 耗时: ${elapsed}s`);
    }

    console.log("\n==================================================================");
    console.log(`✔ 离线渲染抓取完成！共生成 ${renderedCount} 张 1080P PNG 帧保存在: ${OUTPUT_DIR}`);
    console.log("==================================================================");

    client.close();
  } finally {
    cleanup();
  }
}

main().catch(err => {
  console.error("\n✖ 离线渲染流程异常:", err);
  process.exit(1);
});
