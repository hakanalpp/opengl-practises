#version 330

in vec4 fragColor;
in vec2 fragUV;
in vec3 fragPos;
in vec4 fragNormal;

out vec4 outColor;

uniform vec3 pointLightPos;
uniform vec4 pointLightColor;
uniform float pointLightIntensity;

uniform vec3 directionalLightDir;
uniform vec4 directionalLightColor;
uniform float directionalLightIntensity;

uniform vec3 viewPos;
uniform bool blinn;

uniform float texScale;
uniform sampler2D tex1;
uniform sampler2D tex2;

void main()
{
   vec4 texVal1 = texture(tex1, fragUV);
   vec4 texVal2 = texture(tex2, fragUV);

   // Diffuse
	vec4 pointLightDir = normalize(vec4(pointLightPos - fragPos, 1.0));
	float pointLightNDotL = max(dot(fragNormal, pointLightDir), 0.0);
   
	float directionalLightNDotL = max(dot(fragNormal, normalize(vec4(-directionalLightDir, 0.0))), 0.0);
   
   vec4 pointLightScalar = pointLightColor * pointLightIntensity * pointLightNDotL;
   vec4 directionalLightScalar = directionalLightColor * directionalLightIntensity * directionalLightNDotL;

   vec4 pointSpecular = pointLightScalar+directionalLightScalar;

   // Blinn
   if(blinn) {
      vec4 lightDir = normalize(vec4(pointLightPos - fragPos, 1.0));
      vec4 viewDir  = normalize(vec4(viewPos - fragPos, 1.0));
      vec4 halfwayDir = normalize(lightDir + viewDir);
      float spec = pow(max(dot(fragNormal, halfwayDir), 0.0), 1);
      pointSpecular = pointSpecular * spec;
   }

   if (fragUV.x == -1 || fragUV.y == -1) {
      outColor = fragColor;
   } else {
      outColor = texVal1 * (1-texScale) + texVal2 * (texScale);
   }

   outColor = outColor * pointSpecular;
}