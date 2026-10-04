@echo off
chcp 65001 >nul
echo =======================================================================
echo  西行壮歌 · 丝路与额济纳自驾大环线 电影级视频合成流水线
echo =======================================================================
echo.

:: 1. 检查 Python 环境并生成高保真音频母带
echo [Step 1/3] 正在执行 Python 程序化交响配乐与拟音合成...
python generate_audio.py
if %ERRORLEVEL% NEQ 0 (
    echo [错误] Python 音频合成失败，请检查 Python 3 及 numpy 依赖！
    pause
    exit /b 1
)
echo.

:: 2. 检查 Node.js 环境并执行逐帧无头抓取
echo [Step 2/3] 正在启动无头浏览器 (Chrome/Edge) 逐帧抓取 1080P PNG 图像...
echo 提示：如需抓取全量 3600 帧 (120秒)，请使用: node render_video.js --start 0 --end 3599 --out frames
echo 正在渲染演示帧区间 (Frame 0 ~ 120)...
node render_video.js --start 0 --end 120 --out frames
if %ERRORLEVEL% NEQ 0 (
    echo [错误] 无头渲染抓取失败！
    pause
    exit /b 1
)
echo.

:: 3. 检查 FFmpeg 并压制 1080P 30fps H.264/AAC MP4
echo [Step 3/3] 正在检测 FFmpeg 视频压制工具...
set FFMPEG_BIN=
where ffmpeg >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    set FFMPEG_BIN=ffmpeg
) else (
    for /d %%D in ("%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg.Essentials_*") do (
        if exist "%%D\ffmpeg-*\bin\ffmpeg.exe" (
            for /f "delims=" %%F in ('dir /b /s "%%D\ffmpeg.exe"') do set FFMPEG_BIN="%%F"
        )
    )
)

if defined FFMPEG_BIN (
    echo 找到 FFmpeg: %FFMPEG_BIN%
    echo 正在执行电影级高码率压制 (1080P 30fps H.264 High Profile / 320k AAC)...
    %FFMPEG_BIN% -y -framerate 30 -start_number 0 -i frames/frame_%%04d.png -i soundtrack.wav -c:v libx264 -pix_fmt yuv420p -preset slow -crf 18 -c:a aac -b:a 320k -shortest silkroad_epic_1080p.mp4
    if %ERRORLEVEL% EQU 0 (
        echo.
        echo =======================================================================
        echo ✔ 电影级视频合成圆满成功！
        echo 产物文件: silkroad_epic_1080p.mp4 (1080P 30fps Stereo)
        echo =======================================================================
    ) else (
        echo [错误] FFmpeg 压制过程发生异常！
    )
) else (
    echo.
    echo -----------------------------------------------------------------------
    echo [提示] 本机当前未检测到 ffmpeg 命令。
    echo 解决方案 1 (推荐一行命令安装):
    echo    winget install Gyan.FFmpeg.Essentials
    echo.
    echo 解决方案 2 (免安装浏览器直出):
    echo    直接双击打开 video_renderer.html，点击界面右下角
    echo    【🎬 录制整段视频 (WebM/MP4)】按钮，即可在浏览器内 0 依赖录制导出！
    echo.
    echo 解决方案 3 (手动合成命令):
    echo    ffmpeg -y -framerate 30 -start_number 0 -i frames/frame_%%%%04d.png -i soundtrack.wav -c:v libx264 -pix_fmt yuv420p -preset slow -crf 18 -c:a aac -b:a 320k -shortest silkroad_epic_1080p.mp4
    echo -----------------------------------------------------------------------
)

echo.
pause
