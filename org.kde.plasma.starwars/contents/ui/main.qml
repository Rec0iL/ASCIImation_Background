import QtQuick
import org.kde.plasma.plasmoid
import Qt5Compat.GraphicalEffects
import "./code/animations.js" as AnimData

WallpaperItem {
    id: root

    // Resolved configuration values
    readonly property int animIdx: root.configuration.AnimationIndex
    readonly property color phosphorColor: root.configuration.PhosphorColor
    readonly property real glowIntensity: root.configuration.GlowIntensity
    readonly property bool enableScanlines: root.configuration.EnableScanlines
    readonly property real scanlineOpacity: root.configuration.ScanlineOpacity
    readonly property bool enableStarfield: root.configuration.EnableStarfield
    readonly property int starCount: root.configuration.StarCount
    readonly property real playbackSpeed: Math.max(0.2, root.configuration.PlaybackSpeed)
    readonly property string fontFamily: root.configuration.FontFamily
    readonly property bool autoFit: root.configuration.AutoFit
    readonly property int customFontSize: root.configuration.CustomFontSize

    // Is the Nyan Cat animation selected with Default (White) color?
    readonly property bool isNyanRainbow: root.animIdx === 1 && Qt.colorEqual(root.phosphorColor, "#ffffff")

    // Is the Fireworks animation selected with Default (White) color?
    readonly property bool isFireworksColor: root.animIdx === 7 && Qt.colorEqual(root.phosphorColor, "#ffffff")

    // Rainbow palette for Nyan Cat trail lines
    readonly property var rainbowColors: [
        "#ff4444", // Red
        "#ff8800", // Orange
        "#ffdd00", // Yellow
        "#44ff44", // Green
        "#4488ff", // Blue
        "#cc44ff"  // Purple
    ]

    property var activeFrames: []
    property int frameIndex: 0
    property string currentFrameText: ""
    property string displayText: ""
    property bool useRichText: false
    property real computedPixelSize: autoFit ? Math.max(10, Math.min(root.width / 45.0, root.height / 17.0)) : customFontSize

    // Convert a plain-text frame to HTML with rainbow-colored lines for Nyan Cat
    function rainbowifyFrame(plainText) {
        var lines = plainText.split("\n");
        var htmlLines = [];
        // Rainbow colors cycle per non-empty content line
        var colorIdx = 0;
        for (var i = 0; i < lines.length; i++) {
            var line = lines[i];
            // Escape HTML entities
            var escaped = line.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/ /g, "&nbsp;");
            // Check if this line has rainbow trail characters
            var hasTrail = /[~=\-_]{4,}/.test(line);
            if (hasTrail && line.trim().length > 0) {
                var c = rainbowColors[colorIdx % rainbowColors.length];
                htmlLines.push("<span style='color:" + c + ";'>" + escaped + "</span>");
                colorIdx++;
            } else if (line.trim().length > 0) {
                // Cat body / stars — keep white
                htmlLines.push("<span style='color:#ffffff;'>" + escaped + "</span>");
            } else {
                htmlLines.push(escaped);
            }
        }
        return "<pre style='font-family:" + root.fontFamily + ";line-height:1.05;'>" + htmlLines.join("<br>") + "</pre>";
    }

    function colorizeFireworksFrame(plainText) {
        var lines = plainText.split("\n");
        var htmlLines = [];
        var charMap = {
            '@': "<span style='color:#ff4444;'>@</span>",
            '#': "<span style='color:#ff8800;'>#</span>",
            'O': "<span style='color:#ffdd00;'>O</span>",
            'o': "<span style='color:#44ff44;'>o</span>",
            '+': "<span style='color:#44ffff;'>+</span>",
            '*': "<span style='color:#4488ff;'>*</span>",
            '|': "<span style='color:#aaaaaa;'>|</span>",
            ':': "<span style='color:#888888;'>:</span>",
            '&': "&amp;",
            '<': "&lt;",
            '>': "&gt;",
            ' ': "&nbsp;"
        };
        for (var i = 0; i < lines.length; i++) {
            var line = lines[i];
            var coloredLine = "";
            for (var j = 0; j < line.length; j++) {
                var c = line[j];
                if (charMap[c] !== undefined) {
                    coloredLine += charMap[c];
                } else {
                    coloredLine += c;
                }
            }
            htmlLines.push("<span style='color:#ffffff;'>" + coloredLine + "</span>");
        }
        return "<pre style='font-family:" + root.fontFamily + ";line-height:1.05;'>" + htmlLines.join("<br>") + "</pre>";
    }

    function updateDisplayText() {
        if (root.isNyanRainbow) {
            root.useRichText = true;
            root.displayText = rainbowifyFrame(root.currentFrameText);
        } else if (root.isFireworksColor) {
            root.useRichText = true;
            root.displayText = colorizeFireworksFrame(root.currentFrameText);
        } else {
            root.useRichText = false;
            root.displayText = root.currentFrameText;
        }
    }

    onCurrentFrameTextChanged: updateDisplayText()
    onIsNyanRainbowChanged: updateDisplayText()
    onIsFireworksColorChanged: updateDisplayText()

    function updateActiveAnimation() {
        if (!AnimData.animationLibrary || AnimData.animationLibrary.length === 0) return;
        var validIndex = Math.max(0, Math.min(root.animIdx, AnimData.animationLibrary.length - 1));
        root.activeFrames = AnimData.animationLibrary[validIndex].frames;
        root.frameIndex = 0;
        if (root.activeFrames && root.activeFrames.length > 0) {
            root.currentFrameText = root.activeFrames[0][1];
        }
    }

    onAnimIdxChanged: updateActiveAnimation()

    // Deep space black background
    Rectangle {
        anchors.fill: parent
        color: "#030407"
    }

    // Canvas Starfield Particle Effect
    Canvas {
        id: starfieldCanvas
        anchors.fill: parent
        visible: root.enableStarfield
        property var stars: []

        Component.onCompleted: {
            stars = [];
            for (var i = 0; i < 200; i++) {
                stars.push({
                    x: Math.random() * root.width,
                    y: Math.random() * root.height,
                    size: Math.random() * 2.2 + 0.5,
                    alpha: Math.random() * 0.8 + 0.2,
                    speed: Math.random() * 0.4 + 0.1
                });
            }
            requestPaint();
        }

        onWidthChanged: requestPaint()
        onHeightChanged: requestPaint()

        Timer {
            interval: 50
            running: root.enableStarfield
            repeat: true
            onTriggered: {
                var maxCount = Math.min(starfieldCanvas.stars.length, root.starCount);
                for (var i = 0; i < maxCount; i++) {
                    var s = starfieldCanvas.stars[i];
                    s.y += s.speed;
                    if (s.y > root.height) {
                        s.y = 0;
                        s.x = Math.random() * root.width;
                    }
                }
                starfieldCanvas.requestPaint();
            }
        }

        onPaint: {
            var ctx = getContext("2d");
            ctx.clearRect(0, 0, width, height);
            var maxStars = Math.min(stars.length, root.starCount);
            for (var i = 0; i < maxStars; i++) {
                var s = stars[i];
                ctx.fillStyle = "rgba(230, 240, 255, " + s.alpha + ")";
                ctx.fillRect(s.x, s.y, s.size, s.size);
            }
        }
    }

    // Main ASCII Movie Text Display Area
    Item {
        id: textContainer
        anchors.centerIn: parent
        width: Math.min(parent.width * 0.96, root.computedPixelSize * 48)
        height: Math.min(parent.height * 0.96, root.computedPixelSize * 16)

        // === PHOSPHOR GLOW — 3 stacked bloom layers for full neon at high intensity ===
        // (Glow layers only used for non-rainbow mode; rainbow has its own glow)

        // Layer 1: Wide ambient halo (large blur, soft spread)
        Item {
            id: glowWide
            anchors.centerIn: parent
            width: mainText.paintedWidth + 80
            height: mainText.paintedHeight + 80
            visible: root.glowIntensity > 0.05 && !root.useRichText
            opacity: root.glowIntensity * 0.8

            layer.enabled: visible
            layer.smooth: true
            layer.effect: FastBlur {
                radius: 40
                transparentBorder: true
            }

            Text {
                anchors.centerIn: parent
                text: root.currentFrameText
                font.family: root.fontFamily
                font.pixelSize: root.computedPixelSize
                lineHeight: 1.05
                color: root.phosphorColor
            }
        }

        // Layer 2: Medium bloom (mid blur, builds brightness)
        Item {
            id: glowMid
            anchors.centerIn: parent
            width: mainText.paintedWidth + 48
            height: mainText.paintedHeight + 48
            visible: root.glowIntensity > 0.15 && !root.useRichText
            opacity: root.glowIntensity * 0.9

            layer.enabled: visible
            layer.smooth: true
            layer.effect: FastBlur {
                radius: 20
                transparentBorder: true
            }

            Text {
                anchors.centerIn: parent
                text: root.currentFrameText
                font.family: root.fontFamily
                font.pixelSize: root.computedPixelSize
                lineHeight: 1.05
                color: root.phosphorColor
            }
        }

        // Layer 3: Tight core bloom (small blur, hot center)
        Item {
            id: glowCore
            anchors.centerIn: parent
            width: mainText.paintedWidth + 24
            height: mainText.paintedHeight + 24
            visible: root.glowIntensity > 0.3 && !root.useRichText
            opacity: Math.min(1.0, root.glowIntensity * 1.1)

            layer.enabled: visible
            layer.smooth: true
            layer.effect: FastBlur {
                radius: 8
                transparentBorder: true
            }

            Text {
                anchors.centerIn: parent
                text: root.currentFrameText
                font.family: root.fontFamily
                font.pixelSize: root.computedPixelSize
                lineHeight: 1.05
                color: root.phosphorColor
            }
        }

        // === RAINBOW GLOW for Nyan Cat ===
        Item {
            id: rainbowGlow
            anchors.centerIn: parent
            width: mainText.paintedWidth + 60
            height: mainText.paintedHeight + 60
            visible: root.glowIntensity > 0.05 && root.useRichText
            opacity: root.glowIntensity * 0.9

            layer.enabled: visible
            layer.smooth: true
            layer.effect: FastBlur {
                radius: 24
                transparentBorder: true
            }

            Text {
                anchors.centerIn: parent
                text: root.displayText
                textFormat: Text.RichText
                font.family: root.fontFamily
                font.pixelSize: root.computedPixelSize
            }
        }

        // Main Crisp Text Layer
        Text {
            id: mainText
            anchors.centerIn: parent
            text: root.displayText
            textFormat: root.useRichText ? Text.RichText : Text.PlainText
            font.family: root.fontFamily
            font.pixelSize: root.computedPixelSize
            lineHeight: root.useRichText ? 1.0 : 1.05
            color: root.useRichText ? "transparent" : root.phosphorColor
            horizontalAlignment: Text.AlignLeft
            verticalAlignment: Text.AlignVCenter
        }
    }

    // CRT Scanlines Canvas Overlay
    Canvas {
        id: scanlineCanvas
        anchors.fill: parent
        visible: root.enableScanlines
        opacity: root.scanlineOpacity

        onPaint: {
            var ctx = getContext("2d");
            ctx.clearRect(0, 0, width, height);
            ctx.fillStyle = "rgba(0, 0, 0, 0.4)";
            for (var y = 0; y < height; y += 4) {
                ctx.fillRect(0, y, width, 2);
            }
        }

        onWidthChanged: requestPaint()
        onHeightChanged: requestPaint()
    }

    // Soft Vignette Screen Border Overlay
    Rectangle {
        anchors.fill: parent
        color: "transparent"
        border.color: "#000000"
        border.width: Math.max(1, Math.round(Math.min(root.width, root.height) * 0.02))
        opacity: 0.7
    }

    // Animation Loop Timer
    Timer {
        id: frameTimer
        running: true
        repeat: false
        interval: 66

        onTriggered: {
            if (!root.activeFrames || root.activeFrames.length === 0) return;

            root.frameIndex = (root.frameIndex + 1) % root.activeFrames.length;
            var currentFrameData = root.activeFrames[root.frameIndex];
            var delayTicks = currentFrameData[0];
            root.currentFrameText = currentFrameData[1];

            // 1 tick = 66.67 ms (15 FPS base asciimation rate)
            var baseMs = delayTicks * 66.67;
            var nextInterval = Math.max(16, Math.round(baseMs / root.playbackSpeed));

            frameTimer.interval = nextInterval;
            frameTimer.start();
        }
    }

    Component.onCompleted: {
        updateActiveAnimation();
        if (root.activeFrames && root.activeFrames.length > 0) {
            var firstFrame = root.activeFrames[0];
            frameTimer.interval = Math.max(16, Math.round((firstFrame[0] * 66.67) / root.playbackSpeed));
            frameTimer.start();
        }
    }
}
