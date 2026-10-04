<#
.SYNOPSIS
    Silk Road & Ejina Grand Loop Cinematic Video Pipeline (PowerShell)
#>

param(
    [int]$StartFrame = 0,
    [int]$EndFrame = 120,
    [int]$Step = 1,
    [string]$OutDir = "frames",
    [switch]$SkipAudio = $false,
    [switch]$FullRender = $false
)

$ErrorActionPreference = "Stop"

Write-Host "=======================================================================" -ForegroundColor Cyan
Write-Host " Silk Road Expedition - Cinematic Video Generation Pipeline" -ForegroundColor Yellow
Write-Host "=======================================================================" -ForegroundColor Cyan

if ($FullRender) {
    $StartFrame = 0
    $EndFrame = 3599
    Write-Host "[Full Render Mode] Frames: 0 -> 3599 (120 seconds / 3600 frames)" -ForegroundColor Green
}

# 1. Audio Synthesis
if (-not $SkipAudio) {
    Write-Host "`n[Step 1/3] Synthesizing 120s 48kHz stereo master audio..." -ForegroundColor Magenta
    python generate_audio.py
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Audio synthesis failed. Please check Python 3 and numpy."
    }
} else {
    Write-Host "`n[Step 1/3] Skipping audio generation." -ForegroundColor DarkGray
}

# 2. Headless Frame Capture
Write-Host "`n[Step 2/3] Launching headless browser to capture 1080P PNG frames..." -ForegroundColor Magenta
Write-Host "Range: Frame $StartFrame -> Frame $EndFrame (Step: $Step), Output: $OutDir" -ForegroundColor Cyan
node render_video.js --start $StartFrame --end $EndFrame --step $Step --out $OutDir
if ($LASTEXITCODE -ne 0) {
    Write-Error "Headless frame capture failed."
}

# 3. FFmpeg Video Encoding
Write-Host "`n[Step 3/3] Locating FFmpeg encoder..." -ForegroundColor Magenta
$ffmpegExe = $null
$ffmpegCmd = Get-Command "ffmpeg" -ErrorAction SilentlyContinue
if ($ffmpegCmd) {
    $ffmpegExe = $ffmpegCmd.Source
} else {
    $wingetFfmpeg = Get-ChildItem -Path "$env:LOCALAPPDATA\Microsoft\WinGet\Packages" -Filter "ffmpeg.exe" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($wingetFfmpeg) {
        $ffmpegExe = $wingetFfmpeg.FullName
    }
}

if ($ffmpegExe) {
    Write-Host "Found FFmpeg: $ffmpegExe" -ForegroundColor Green
    Write-Host "Encoding 1080P 30fps H.264 / AAC MP4 video..." -ForegroundColor Cyan

    $renderedCount = [math]::Floor(($EndFrame - $StartFrame) / $Step) + 1
    $durationSec = [math]::Round($renderedCount / 30.0, 3)
    $audioStartSec = [math]::Round($StartFrame / 30.0, 3)

    $ffmpegArgs = @(
        "-y",
        "-framerate", "30",
        "-start_number", "$StartFrame",
        "-i", "$OutDir/frame_%04d.png"
    )

    if (Test-Path "soundtrack.wav") {
        if ($StartFrame -gt 0) {
            $ffmpegArgs += @("-ss", "$audioStartSec")
        }
        $ffmpegArgs += @("-i", "soundtrack.wav")
    }

    $ffmpegArgs += @(
        "-t", "$durationSec",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "slow",
        "-crf", "18"
    )

    if (Test-Path "soundtrack.wav") {
        $ffmpegArgs += @("-c:a", "aac", "-b:a", "320k", "-shortest")
    }

    $ffmpegArgs += "silkroad_epic_1080p.mp4"

    & $ffmpegExe @ffmpegArgs
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n=======================================================================" -ForegroundColor Green
        Write-Host "✔ Video generated successfully: silkroad_epic_1080p.mp4" -ForegroundColor Yellow
        Write-Host "=======================================================================" -ForegroundColor Green
    } else {
        Write-Warning "FFmpeg exited with error code: $LASTEXITCODE"
    }
} else {
    Write-Host "`n-----------------------------------------------------------------------" -ForegroundColor Yellow
    Write-Host "[Note] ffmpeg is not currently in system PATH." -ForegroundColor White
    Write-Host "Option 1 (Install via winget):" -ForegroundColor Cyan
    Write-Host "   winget install Gyan.FFmpeg.Essentials" -ForegroundColor Green
    Write-Host "`nOption 2 (Direct browser export):" -ForegroundColor Cyan
    Write-Host "   Open video_renderer.html in Chrome/Edge, click the Record button on bottom dock." -ForegroundColor Green
    Write-Host "-----------------------------------------------------------------------" -ForegroundColor Yellow
}
