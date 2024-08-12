let n, speed, minSize, maxSize, r, g, b
let xpos = []
let ypos = []
let size = []
let self = []

function setup() {
  createCanvas(600, 500);
  minSize = 75
  maxSize = 75
  speed = 1.5
  r = 212
  g = 241
  b = 249
  n = 0
  noFill()
  strokeWeight(1)
  xpos[0] = round(random(0, width))
  ypos[0] = round(random(0, height))
  size[0] = 0
  self[0] = round(random(minSize, maxSize))
}

function draw() {
  n = n + 1
  background(r, g, b);
  for (i = 0; i < n; i++) {
    size[i] = size[i] + speed
    if (size[i] < self[i]) {
      stroke(r * size[i] / self[i], g * size[i] / self[i], b * size[i] / self[i])
      circle(xpos[i], ypos[i], size[i])
    }
  }
  xpos[n] = round(random(0, width))
  ypos[n] = round(random(0, height))
  size[n] = 0
  self[n] = round(random(minSize, maxSize))
}
