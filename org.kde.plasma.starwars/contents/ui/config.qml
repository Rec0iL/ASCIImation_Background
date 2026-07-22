import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs
import org.kde.kirigami as Kirigami

Kirigami.FormLayout {
    id: root
    twinFormLayouts: parentLayout
    property alias formLayout: root

    // cfg_ properties auto-synced by KDE config system to wallpaper.configuration
    property int cfg_AnimationIndex: wallpaper.configuration.AnimationIndex
    property int cfg_ThemeIndex: wallpaper.configuration.ThemeIndex
    property color cfg_PhosphorColor: wallpaper.configuration.PhosphorColor
    property double cfg_GlowIntensity: wallpaper.configuration.GlowIntensity
    property bool cfg_EnableScanlines: wallpaper.configuration.EnableScanlines
    property double cfg_ScanlineOpacity: wallpaper.configuration.ScanlineOpacity
    property bool cfg_EnableStarfield: wallpaper.configuration.EnableStarfield
    property int cfg_StarCount: wallpaper.configuration.StarCount
    property double cfg_PlaybackSpeed: wallpaper.configuration.PlaybackSpeed
    property string cfg_FontFamily: wallpaper.configuration.FontFamily
    property bool cfg_AutoFit: wallpaper.configuration.AutoFit
    property int cfg_CustomFontSize: wallpaper.configuration.CustomFontSize

    readonly property var themeColors: [
        "#ffffff", // Default (White)
        "#ffb000", // Amber CRT
        "#00ff66", // Matrix Green
        "#00e5ff", // Cyberpunk Cyan
        "#eeeeee", // Classic Monochrome
        "#ff007f"  // Synthwave Pink
    ]

    Kirigami.Separator {
        Kirigami.FormData.isSection: true
        Kirigami.FormData.label: "ASCII Movie & Animation"
    }

    ComboBox {
        id: animCombo
        Kirigami.FormData.label: "Animation Scene:"
        model: [
            "🎬 Star Wars Episode IV (Full Movie)",
            "🐱 Nyan Cat Rainbow Flight",
            "🦜 Party Parrot Dance",
            "🌐 3D Spinning Wireframe Cube",
            "🟢 Matrix Digital Rain",
            "🐟 ASCII Aquarium",
            "🍩 Rotating Donut (Torus)",
            "🎆 Fireworks Display",
            "📀 DVD Bouncing Logo",
            "〰️ Sine Wave Oscillator",
            "🌍 Rotating Wireframe Globe"
        ]
        currentIndex: cfg_AnimationIndex
        onCurrentIndexChanged: cfg_AnimationIndex = currentIndex
    }

    Kirigami.Separator {
        Kirigami.FormData.isSection: true
        Kirigami.FormData.label: "Visual Aesthetics & Colors"
    }

    ComboBox {
        id: themeCombo
        Kirigami.FormData.label: "Color Preset:"
        model: [
            "Default (White)",
            "Retro Amber CRT",
            "Matrix Green",
            "Cyberpunk Cyan",
            "Classic Monochrome",
            "Synthwave Pink",
            "Custom Color"
        ]
        currentIndex: cfg_ThemeIndex
        onCurrentIndexChanged: {
            cfg_ThemeIndex = currentIndex
            if (currentIndex >= 0 && currentIndex < themeColors.length) {
                cfg_PhosphorColor = themeColors[currentIndex]
            }
        }
    }

    RowLayout {
        Kirigami.FormData.label: "Phosphor Color:"
        Rectangle {
            width: 24
            height: 24
            radius: 4
            color: cfg_PhosphorColor
            border.color: Kirigami.Theme.textColor
            border.width: 1
        }
        Button {
            text: "Pick Custom Color..."
            onClicked: colorDialog.open()
        }
    }

    RowLayout {
        Kirigami.FormData.label: "Phosphor Glow:"
        Slider {
            id: glowSlider
            from: 0.0
            to: 1.0
            stepSize: 0.05
            value: cfg_GlowIntensity
            onValueChanged: cfg_GlowIntensity = value
            Layout.preferredWidth: Kirigami.Units.gridUnit * 12
        }
        Label {
            text: Math.round(cfg_GlowIntensity * 100) + "%"
        }
    }

    Kirigami.Separator {
        Kirigami.FormData.isSection: true
        Kirigami.FormData.label: "CRT & Screen Effects"
    }

    CheckBox {
        id: scanlinesCheck
        Kirigami.FormData.label: "CRT Overlay:"
        text: "Enable CRT Scanlines"
        checked: cfg_EnableScanlines
        onCheckedChanged: cfg_EnableScanlines = checked
    }

    RowLayout {
        visible: scanlinesCheck.checked
        Kirigami.FormData.label: "Scanline Intensity:"
        Slider {
            id: scanlineSlider
            from: 0.05
            to: 0.80
            stepSize: 0.05
            value: cfg_ScanlineOpacity
            onValueChanged: cfg_ScanlineOpacity = value
            Layout.preferredWidth: Kirigami.Units.gridUnit * 12
        }
        Label {
            text: Math.round(cfg_ScanlineOpacity * 100) + "%"
        }
    }

    CheckBox {
        id: starfieldCheck
        Kirigami.FormData.label: "Background:"
        text: "Enable Space Starfield Particle Effect"
        checked: cfg_EnableStarfield
        onCheckedChanged: cfg_EnableStarfield = checked
    }

    RowLayout {
        visible: starfieldCheck.checked
        Kirigami.FormData.label: "Star Count:"
        Slider {
            id: starCountSlider
            from: 50
            to: 400
            stepSize: 10
            value: cfg_StarCount
            onValueChanged: cfg_StarCount = Math.round(value)
            Layout.preferredWidth: Kirigami.Units.gridUnit * 12
        }
        Label {
            text: Math.round(cfg_StarCount)
        }
    }

    Kirigami.Separator {
        Kirigami.FormData.isSection: true
        Kirigami.FormData.label: "Playback & Typography"
    }

    RowLayout {
        Kirigami.FormData.label: "Playback Speed:"
        Slider {
            id: speedSlider
            from: 0.5
            to: 2.5
            stepSize: 0.1
            value: cfg_PlaybackSpeed
            onValueChanged: cfg_PlaybackSpeed = Math.round(value * 10) / 10
            Layout.preferredWidth: Kirigami.Units.gridUnit * 12
        }
        Label {
            text: cfg_PlaybackSpeed.toFixed(1) + "x"
        }
    }

    ComboBox {
        id: fontCombo
        Kirigami.FormData.label: "Font Family:"
        model: ["Monospace", "Hack", "JetBrains Mono", "Fira Code", "Source Code Pro", "Courier New"]
        currentIndex: model.indexOf(cfg_FontFamily) >= 0 ? model.indexOf(cfg_FontFamily) : 0
        onCurrentTextChanged: cfg_FontFamily = currentText
    }

    CheckBox {
        id: autoFitCheck
        Kirigami.FormData.label: "Sizing:"
        text: "Auto-fit text to screen size"
        checked: cfg_AutoFit
        onCheckedChanged: cfg_AutoFit = checked
    }

    RowLayout {
        visible: !autoFitCheck.checked
        Kirigami.FormData.label: "Font Size:"
        SpinBox {
            from: 8
            to: 72
            value: cfg_CustomFontSize
            onValueChanged: cfg_CustomFontSize = value
        }
        Label { text: "px" }
    }

    ColorDialog {
        id: colorDialog
        title: "Choose Phosphor Text Color"
        onAccepted: {
            cfg_PhosphorColor = colorDialog.selectedColor
            cfg_ThemeIndex = 6 // Custom Color
        }
    }
}
