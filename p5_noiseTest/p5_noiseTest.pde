// PERLIN NOISE TEST

// JAVA byte => -127 -> 128. Overflow loops back.


float[] rocksX;
float[] rocksY;
int rockCount = 200;

float noiseX, noiseXIncrement, windowXincrement;
float noiseY, noiseYIncrement, windowYIncrement;


void setup() {
  size(255, 255);
  //rectMode(CENTER);

  rocksX = new float[rockCount];
  rocksY = new float[rockCount];

  for (int i=0; i< rocksX.length; i++) {
    rocksX[i] = (int)random(width);
    rocksY[i] = (int)random(height);
    
    //rocksX[i] = (width / (float)rocksX.length) * i;
    //rocksY[i] = int(height * 0.5);
  }

  noiseX = random(1);
  noiseY = random(1);
  noiseXIncrement = 0.01;
  noiseYIncrement = 0.01;

  windowXincrement = 1;
  windowYIncrement = 1;
  

}

void draw() {
  background(0);

  fill(255);
  noStroke();
  for (int i=0; i< rocksX.length; i++) {
    float rockNoisePosX = map(rocksX[i], 0, width, noiseX, noiseX + windowXincrement);
    float rockNoisePosY = map(rocksY[i], 0, height, noiseY, noiseY + windowYIncrement);

    float value = noise(rockNoisePosX, rockNoisePosY) * 20;
    //println(value);
    ellipse(rocksX[i], rocksY[i], value, value);
    //rect(rocksX[i], rocksY[i],(width / (float)rocksX.length), -value);
  }

  noiseX += noiseXIncrement;
  noiseY += noiseYIncrement;
}