# 隐藏PowerShell窗口
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;

public class Win32 {
    [DllImport("kernel32.dll")]
    public static extern IntPtr GetConsoleWindow();

    [DllImport("user32.dll")]
    public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);

    public const int SW_HIDE = 0;
    public const int SW_SHOW = 5;
}
"@

$consolePtr = [Win32]::GetConsoleWindow()
# 隐藏窗口
[Win32]::ShowWindow($consolePtr, [Win32]::SW_HIDE)

# 定义保存截图的目录和路径
$outputDir = "C:\Screenshots"
if (!(Test-Path -Path $outputDir)) {
    New-Item -Path $outputDir -ItemType Directory
}

# 定义保存截图的文件路径
$outputFile = "$outputDir\screenshot.png"

# 加载必要的程序集
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# 获取屏幕尺寸
$Screen = [System.Windows.Forms.SystemInformation]::VirtualScreen
$Width = $Screen.Width
$Height = $Screen.Height

# 创建 Bitmap 对象来存储屏幕截图
$Bitmap = New-Object System.Drawing.Bitmap $Width, $Height
$Graphics = [System.Drawing.Graphics]::FromImage($Bitmap)

# 进行屏幕截图
$Graphics.CopyFromScreen($Screen.Left, $Screen.Top, 0, 0, $Bitmap.Size)

# 保存截图
$Bitmap.Save($outputFile, [System.Drawing.Imaging.ImageFormat]::Png)

# 清理
$Graphics.Dispose()
$Bitmap.Dispose()

Write-Host "Screenshot saved to $outputFile"

# 显示窗口（可选，如果你想在完成截图后显示）
# [Win32]::ShowWindow($consolePtr, [Win32]::SW_SHOW)
