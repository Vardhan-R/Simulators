let magn, angle, minMag, maxMag, minAngle, maxAngle, scaleFactor, branches

function setup() {
  createCanvas(650, 500);
  scaleFactor = 1 / 2
  branches = 3
  magn = 240
  angle = 2 * PI / 3
  minMag = 1
  maxMag = 300
  minAngle = 0
  maxAngle = 2 * PI
}

function draw() {
  background(220);
  translate(width / 2, height)
  branches = slider(10 - width / 2, -70, 150, branches, 0, 4)
  scaleFactor = slider(10 - width / 2, -50, 150, scaleFactor, 0, 1)
  magn = slider(10 - width / 2, -30, 150, magn, minMag, maxMag)
  angle = slider(10 - width / 2, -10, 150, angle, minAngle, maxAngle)
  scale(1, -1)
  fractal(magn, angle)
}

function fractal(m, ang) {
  if (m > 1) {
    stroke(0)
    line(0, 0, 0, m)
    m *= scaleFactor
    push()
    translate(0, m / scaleFactor)
    rotate(((branches - 1) * ang) / 2)
    fractal(m, ang)
    for (let i = 0; i < branches - 1; i++) {
      rotate(-ang)
      fractal(m, ang)
    }
    pop()
  }
}

function slider(sliderX, sliderY, sliderL, thing, minVal, maxVal) {
  if (mouseIsPressed) {
    if (sliderX <= mouseX - width / 2 && mouseX - width / 2 <= sliderX + sliderL && sliderY - 5 <= mouseY - height && mouseY - height <= sliderY + 5) {
      thing = map(mouseX - width / 2, sliderX, sliderX + sliderL, minVal, maxVal)
    }
  }
  textAlign(CENTER)
  strokeWeight(1)
  stroke(0, 255, 0)
  line(sliderX, sliderY, sliderX + sliderL, sliderY)

  noStroke()
  fill(255, 255, 0)
  text(minVal, sliderX, sliderY)
  text(maxVal, sliderX + sliderL, sliderY)

  fill(255, 0, 0)
  circle(map(thing, minVal, maxVal, sliderX, sliderX + sliderL), sliderY, 10)

  fill(255, 255, 0)
  text(thing, map(thing, minVal, maxVal, sliderX, sliderX + sliderL), sliderY)

  return (thing)
}
