# process-image.ps1 - Windows built-in engine handler (System.Drawing, no install needed)
param(
  [Parameter(Mandatory=$true)][string]$InputImage,
  [string]$Output,
  [int]$Compress = 85,
  [string]$Resize,
  [string]$Convert,
  [string]$Crop,
  [int]$Rotate,
  [string]$Flip,
  [switch]$Grayscale,
  [string]$Watermark,
  [int]$Round
)
$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing
$img = [System.Drawing.Image]::FromFile($InputImage)
$w = $img.Width; $h = $img.Height
$ext = [IO.Path]::GetExtension($InputImage).TrimStart(".").ToLower()
if (-not $Output) { $outExt = $ext; if ($Convert) { $outExt = $Convert.ToLower() }; $Output = [IO.Path]::ChangeExtension($InputImage, $outExt) }

# --- crop ---
if ($Crop) {
  $p = $Crop.Split(":"); $x=[int]$p[0]; $y=[int]$p[1]; $cw=[int]$p[2]; $ch=[int]$p[3]
  $b = New-Object System.Drawing.Bitmap($cw,$ch)
  $gc = [System.Drawing.Graphics]::FromImage($b)
  $srcRect = New-Object System.Drawing.Rectangle($x,$y,$cw,$ch)
  $gc.DrawImage($img,(New-Object System.Drawing.Rectangle(0,0,$cw,$ch)),$srcRect,[System.Drawing.GraphicsUnit]::Pixel)
  $gc.Dispose(); $img.Dispose(); $img=$b; $w=$cw; $h=$ch
}
# --- resize ---
if ($Resize) {
  $sz = $Resize.Split("x"); $nw = if ($sz[0] -eq "-1") { -1 } else { [int]$sz[0] }; $nh = if ($sz[1] -eq "-1") { -1 } else { [int]$sz[1] }
  if ($nw -eq -1) { $nw = [int]([double]$w * ($nh / $h)) }
  if ($nh -eq -1) { $nh = [int]([double]$h * ($nw / $w)) }
  $b = New-Object System.Drawing.Bitmap($nw,$nh)
  $gr = [System.Drawing.Graphics]::FromImage($b)
  $gr.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
  $gr.DrawImage($img,0,0,$nw,$nh); $gr.Dispose(); $img.Dispose(); $img=$b; $w=$nw; $h=$nh
}
# --- rotate ---
if ($Rotate) {
  $rt = [System.Drawing.RotateFlipType]::Rotate90FlipNone
  if ($Rotate -eq 180) { $rt = [System.Drawing.RotateFlipType]::Rotate180FlipNone }
  elseif ($Rotate -eq 270) { $rt = [System.Drawing.RotateFlipType]::Rotate270FlipNone }
  $img.RotateFlip($rt); $w=$img.Width; $h=$img.Height
}
# --- flip ---
if ($Flip) {
  if ($Flip -eq "h") { $img.RotateFlip([System.Drawing.RotateFlipType]::RotateNoneFlipX) }
  elseif ($Flip -eq "v") { $img.RotateFlip([System.Drawing.RotateFlipType]::RotateNoneFlipY) }
}
# --- grayscale ---
if ($Grayscale) {
  $b = New-Object System.Drawing.Bitmap($img.Width,$img.Height)
  $gg = [System.Drawing.Graphics]::FromImage($b)
  $cm = New-Object System.Drawing.Imaging.ColorMatrix
  $cm.Matrix00=0.299; $cm.Matrix10=0.587; $cm.Matrix20=0.114
  $cm.Matrix01=0.299; $cm.Matrix11=0.587; $cm.Matrix21=0.114
  $cm.Matrix02=0.299; $cm.Matrix12=0.587; $cm.Matrix22=0.114
  $ia = New-Object System.Drawing.Imaging.ImageAttributes
  $ia.SetColorMatrix($cm)
  $full = New-Object System.Drawing.Rectangle(0,0,$img.Width,$img.Height)
  $gg.DrawImage($img,$full,0,0,$img.Width,$img.Height,[System.Drawing.GraphicsUnit]::Pixel,$ia)
  $gg.Dispose(); $img.Dispose(); $img=$b; $ia.Dispose()
}
# --- watermark ---
if ($Watermark) {
  $b = New-Object System.Drawing.Bitmap($img.Width,$img.Height)
  $gw = [System.Drawing.Graphics]::FromImage($b)
  $gw.DrawImage($img,0,0,$img.Width,$img.Height)
  $fsize = [Math]::Max(16,[int]($img.Width/15))
  $font = New-Object System.Drawing.Font("Arial",$fsize)
  $brush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(150,255,255,255))
  $gw.DrawString($Watermark,$font,$brush,$img.Width-[int]($img.Width*0.85),$img.Height-[int]($img.Height*0.9))
  $gw.Dispose(); $img.Dispose(); $img=$b
}
# --- round (transparent corners) ---
if ($Round) {
  $b = New-Object System.Drawing.Bitmap($img.Width,$img.Height,[System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
  $gr2 = [System.Drawing.Graphics]::FromImage($b)
  $gr2.Clear([System.Drawing.Color]::Transparent)
  $d = $Round*2
  $path = New-Object System.Drawing.Drawing2D.GraphicsPath
  $path.AddArc(0,0,$d,$d,180,90)
  $path.AddArc($img.Width-$d,0,$d,$d,270,90)
  $path.AddArc($img.Width-$d,$img.Height-$d,$d,$d,0,90)
  $path.AddArc(0,$img.Height-$d,$d,$d,90,90)
  $path.CloseFigure()
  $gr2.SetClip($path)
  $gr2.DrawImage($img,0,0); $gr2.Dispose(); $img.Dispose(); $img=$b
}
# --- save (format by extension) ---
$outExt = [IO.Path]::GetExtension($Output).TrimStart(".").ToLower()
$fmtMap = @{ jpg="image/jpeg"; jpeg="image/jpeg"; png="image/png"; bmp="image/bmp"; gif="image/gif" }
if (-not $fmtMap.ContainsKey($outExt)) { throw "System.Drawing 不支持的输出格式: $outExt (png/jpg/bmp/gif)" }
$codec = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object { $_.MimeType -eq $fmtMap[$outExt] }
if (-not $codec) { throw "找不到编码器: $($fmtMap[$outExt])" }
if ($outExt -in @("jpg","jpeg")) {
  $ep = New-Object System.Drawing.Imaging.EncoderParameters 1
  $ep.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter([System.Drawing.Imaging.Encoder]::Quality,[long]$Compress)
  $img.Save($Output,$codec,$ep); $ep.Dispose()
} elseif ($outExt -eq "png") {
  $img.Save($Output,[System.Drawing.Imaging.ImageFormat]::Png)
} elseif ($outExt -eq "bmp") {
  $img.Save($Output,[System.Drawing.Imaging.ImageFormat]::Bmp)
} elseif ($outExt -eq "gif") {
  $img.Save($Output,[System.Drawing.Imaging.ImageFormat]::Gif)
} else {
  $img.Save($Output)
}
$img.Dispose()
Write-Output "OK $Output"