#version 440

layout(location = 0) in vec2 qt_TexCoord0;
layout(location = 0) out vec4 fragColor;

layout(binding = 1) uniform sampler2D source;

layout(std140, binding = 0) uniform buf {
    mat4 qt_Matrix;
    float qt_Opacity;
    float enableDistortion;
    float enableVignette;
};

void main() {
    vec2 uv = qt_TexCoord0;
    
    if (enableDistortion > 0.5) {
        vec2 cc = uv - 0.5;
        float dist = dot(cc, cc);
        uv = uv + cc * (dist * 0.25);
    }
    
    if (uv.x < 0.0 || uv.x > 1.0 || uv.y < 0.0 || uv.y > 1.0) {
        fragColor = vec4(0.0, 0.0, 0.0, 1.0);
        return;
    }
    
    vec4 color = texture(source, uv);
    
    if (enableVignette > 0.5) {
        vec2 cc = qt_TexCoord0 - 0.5;
        float vignette = 1.0 - dot(cc, cc) * 2.5;
        vignette = clamp(vignette, 0.0, 1.0);
        color.rgb *= vignette;
    }
    
    fragColor = color * qt_Opacity;
}
