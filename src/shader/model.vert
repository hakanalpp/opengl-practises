#version 330

layout(location = 0) in vec4 vertexPosition;
layout(location = 1) in vec4 vertexColor;
layout(location = 2) in vec2 vertexUV;
layout(location = 3) in vec4 vertexNormal;

out vec4 fragColor;
out vec2 fragUV;
out vec3 fragPos;
out vec4 fragNormal;

uniform mat4 view;
uniform mat4 proj;

void main()
{
	gl_Position = proj * view * vertexPosition;
	fragPos = vec3(vertexPosition);
	fragColor = vertexColor;
	fragUV = vertexUV;
	fragNormal = normalize(vertexNormal);
}