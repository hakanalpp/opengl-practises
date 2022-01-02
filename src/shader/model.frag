#version 330

in vec4 fragColor;
in vec2 fragUV;
in vec3 fragPos;
in vec4 fragNormal;

out vec4 outColor;

// I did not give the light params as list, because it is easier to check my program this way.

uniform vec3 pointLightPos;
uniform vec4 pointLightColor;
uniform float pointLightIntensity;

uniform vec3 directionalLightDir;
uniform vec4 directionalLightColor;
uniform float directionalLightIntensity;

uniform vec3 spotLightPos;
uniform vec3 spotLightDir;
uniform vec4 spotLightColor;
uniform float spotLightIntensity;
uniform float spotLightAngle;

uniform vec3 viewPos;
uniform bool blinn;

uniform float texScale;
uniform sampler2D tex1;
uniform sampler2D tex2;

void main()
{
   vec4 texVal1 = texture(tex1, fragUV);
   vec4 texVal2 = texture(tex2, fragUV);

   // Lambert

   // Point Light
	vec4 pointLightDir = normalize(vec4(pointLightPos - fragPos, 1.0));
	float pointLightNDotL = max(dot(fragNormal, pointLightDir), 0.0);
   vec4 pointLightScalar = pointLightColor * pointLightIntensity * pointLightNDotL;

   // Directional Light
	float directionalLightNDotL = max(dot(fragNormal, normalize(vec4(-directionalLightDir, 0.0))), 0.0);
   vec4 directionalLightScalar = directionalLightColor * directionalLightIntensity * directionalLightNDotL;

   // Spot Light
   vec4 spotLightScalar = vec4(0,0,0,1);
   float angleThreshold = dot(normalize(spotLightPos-fragPos), normalize(-spotLightDir));
   if (angleThreshold >= spotLightAngle) {
      spotLightScalar = spotLightColor * spotLightIntensity * pow(angleThreshold, 45);
   }

   // Blinn. I only calculated blinn for point light on top.
   float blinnSpec = 0.0;
   if(blinn) {
      vec4 lightDir = normalize(vec4(pointLightPos - fragPos, 1.0));
      vec4 viewDir  = normalize(vec4(viewPos - fragPos, 1.0));
      vec4 halfwayDir = normalize(lightDir + viewDir);
      blinnSpec = pow(max(dot(fragNormal, halfwayDir), 0.0), 2);
   }

   vec4 pointSpecular = pointLightScalar + directionalLightScalar + spotLightScalar + blinnSpec;

   if (fragUV.x == -1 || fragUV.y == -1) {
      outColor = fragColor;
   } else {
      outColor = texVal1 * (1-texScale) + texVal2 * (texScale);
   }

   outColor = outColor * pointSpecular;
}