#version 330 core
out vec4 FragColor;

in vec2 TexCoord;

uniform sampler2D texture1;
uniform sampler2D texture2;

void main()
{
    FragColor = (texture(texture1, TexCoord)-texture(texture2, TexCoord)+1)/2; # texture returns 0~1, to avoid negative number, we +1 / 2
}