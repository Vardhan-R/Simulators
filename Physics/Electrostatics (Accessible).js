let gravConst, k, damping, p
let allMasses = []
let allCharges = []
let allColours = []
let allPos = []
let allVel = []
let allAcc = []

let allUHS = []
let allUSS = []



function setup() {
  createCanvas(600, 500);

  gravConst = 1
  k = 1000
  damping = 0
  p = 1

  // createParticle(m, q, r, g, b, px, py, vx, vy)
  // new UHS(m, q, diameter, r, g, b, px, py, vx, vy)
  // new USS(m, q, diameter, r, g, b, px, py, vx, vy)

  createParticle(1, 1, 255, 0, 0, 3 * width / 4, height / 2, 0, -1)
  createParticle(100, -1, 0, 255, 0, width / 2, height / 2, 0, 0)
  // createParticle(1, 4, 255, 255, 0, width / 4, height / 2, 0, 0)
  createParticle(1, 1, 0, 0, 255, width / 4, height / 2, 0, 1)
  // allUHS.push(new UHS(1, 1, 250, 255, 0, 255, 2.5 * width / 6, height / 2, 0, 0))
  // allUHS.push(new UHS(1, 1, 250, 255, 0, 255, width / 4, 3 * height / 4, 0, 0))
  // allUHS.push(new UHS(1, 1, 250, 255, 0, 255, 3 * width / 4, height / 4, 0, 0))
  // allUHS.push(new UHS(1, 1, 250, 255, 0, 255, 3 * width / 4, 3 * height / 4, 0, 0))
  // allUSS.push(new USS(1, -3, 250, 255, 0, 255, 100, width / 2, height / 4, 0, 0))
  // allUSS.push(new USS(1, 1, 250, 255, 0, 255, 100, width / 2, 3 * height / 4, 0, 0))
  // allUSS.push(new USS(1, 1, 250, 255, 0, 255, 100, 3 * width / 4, height / 2, 0, 0))
  // allUSS.push(new USS(1, 1, 250, 255, 0, 255, 100, 2.5 * width / 6, height / 2, 0, 0))
}



function draw() {
  background(0);
  noStroke()
  fill(0, 0, 255)
  text("SPACE", 30, 15)
  text("to Pause", 32, 30)
  text("Damping", 40, 45)
  text("Mass", 110, 15)
  text("Charge", 190, 15)
  text("xPos", 270, 15)
  text("yPos", 350, 15)
  text("xVel", 430, 15)
  text("yVel", 510, 15)
  damping = slider(15, 60, 50, damping, 0, 1)
  for (let i = 0; i < allMasses.length; i++) {
    allMasses[i] = slider(90, 15 * (i + 2), 50, allMasses[i], 1, 100)
    allCharges[i] = slider(170, 15 * (i + 2), 50, allCharges[i], -5, 5)
    allPos[i].x = slider(250, 15 * (i + 2), 50, allPos[i].x, 0, width)
    allPos[i].y = slider(330, 15 * (i + 2), 50, allPos[i].y, 0, height)
    allVel[i].x = slider(410, 15 * (i + 2), 50, allVel[i].x, -5, 5)
    allVel[i].y = slider(490, 15 * (i + 2), 50, allVel[i].y, -5, 5)
  }
  translate(width / 2, height / 2)
  scale(1, -1)
  translate(-width / 2, -height / 2)
  if (p == 1) {
    update()
  }
  show()
  for (let a = 0; a < allUHS.length; a++) {
    allUHS[a].UHS_show()
  }
  for (let a = 0; a < allUSS.length; a++) {
    allUSS[a].USS_show()
  }
  damp()
}



function createParticle(m, q, r, g, b, px, py, vx, vy) {
  allMasses.push(m)
  allCharges.push(q)
  allColours.push(createVector(r, g, b))
  allPos.push(createVector(px, py))
  allVel.push(createVector(vx, vy))
  allAcc.push(createVector(0, 0))
}



function update() {
  // vel and acc update for all the particles
  for (let i = 0; i < allMasses.length; i++) {
    tempAcc = createVector()
    tempAccUHS = createVector()
    for (let j = 0; j < allMasses.length; j++) {
      if (allPos[i] != allPos[j]) {
        acc = k * allCharges[i] * allCharges[j] / ((dist(allPos[i].x, allPos[i].y, allPos[j].x, allPos[j].y)) ** 3) / allMasses[i]
        dir = createVector(allPos[i].x - allPos[j].x, allPos[i].y - allPos[j].y)
        dir.mult(acc)
        tempAcc.add(dir)
      }
    }
    allAcc[i] = tempAcc



    for (let j = 0; j < allUHS.length; j++) {
      if (dist(allPos[i].x, allPos[i].y, allUHS[j].px, allUHS[j].py) > allUHS[j].diameter / 2) {
        acc = k * allCharges[i] * allUHS[j].q / ((dist(allPos[i].x, allPos[i].y, allUHS[j].px, allUHS[j].py)) ** 3) / allMasses[i]
        dir = createVector(allPos[i].x - allUHS[j].px, allPos[i].y - allUHS[j].py)
        dir.mult(acc)
        tempAcc.add(dir)
        dir.mult(allMasses[i] / allUHS[j].m)
        tempAccUHS.add(dir)
        // still have not done acc, vel and mvmnt for UHS
      }
    }



    for (let j = 0; j < allUSS.length; j++) {
      if (dist(allPos[i].x, allPos[i].y, allUSS[j].p.x, allUSS[j].p.y) > allUSS[j].diameter / 2) {
        acc = k * allCharges[i] * allUSS[j].q / ((dist(allPos[i].x, allPos[i].y, allUSS[j].p.x, allUSS[j].p.y)) ** 3) / allMasses[i]
        dir = createVector(allPos[i].x - allUSS[j].p.x, allPos[i].y - allUSS[j].p.y)
        dir.mult(acc)
        tempAcc.add(dir)
      } else {
        acc = 8 * k * allCharges[i] * allUSS[j].q / (allUSS[j].diameter ** 3) / allMasses[i]
        dir = createVector(allPos[i].x - allUSS[j].p.x, allPos[i].y - allUSS[j].p.y)
        dir.mult(acc)
        tempAcc.add(dir)
      }
    }



    allVel[i].add(tempAcc)
  }

  // pos update for all particles
  for (let i = 0; i < allMasses.length; i++) {
    allPos[i].add(allVel[i])
  }
}



function show() {
  stroke(255)
  for (let i = 0; i < allMasses.length; i++) {
    fill(allColours[i].x, allColours[i].y, allColours[i].z)
    circle(allPos[i].x, allPos[i].y, 20)
  }
}



function damp() {
  for (let i = 0; i < allMasses.length; i++) {
    allVel[i].mult(1 - damping)
  }
}



class UHS {
  constructor(m, q, diameter, r, g, b, px, py, vx, vy) {
    this.m = m
    this.q = q
    this.diameter = diameter
    this.r = r
    this.g = g
    this.b = b
    this.px = px
    this.py = py
    this.vx = vx
    this.vy = vy
  }
  
  UHS_show() {
    push()
    noFill()
    stroke(this.r, this.g, this.b)
    circle(this.px, this.py, this.diameter)
    pop()
  }
}



class USS {
  constructor(m, q, diameter, r, g, b, a, px, py, vx, vy) {
    this.m = m
    this.q = q
    this.diameter = diameter
    this.r = r
    this.g = g
    this.b = b
    this.a = a
    this.p = createVector(px, py)
  }
  
  USS_show() {
    push()
    fill(this.r, this.g, this.b ,this.a)
    circle(this.p.x, this.p.y, this.diameter)
    pop()
  }
}



function slider(sliderX, sliderY, sliderL, thing, minVal, maxVal) {
  if (mouseIsPressed) {
    if (sliderX <= mouseX && mouseX <= sliderX + sliderL && sliderY - 5 <= mouseY && mouseY <= sliderY + 5) {
      thing = map(mouseX, sliderX, sliderX + sliderL, minVal, maxVal)
      text(thing, map(thing, minVal, maxVal, sliderX, sliderX + sliderL), sliderY)
    }
  }
  textAlign(CENTER)
  strokeWeight(1)
  stroke(0, 255, 0)
  line(sliderX, sliderY, sliderX + sliderL, sliderY)
  noStroke()
  if (!mouseIsPressed) {
    fill(255, 255, 0)
    text(minVal, sliderX, sliderY)
    text(maxVal, sliderX + sliderL, sliderY)
  }

  fill(255, 0, 0)
  circle(map(thing, minVal, maxVal, sliderX, sliderX + sliderL), sliderY, 10)

  fill(255, 255, 0)

  return (thing)
}



function keyPressed() {
  if (keyCode === 32) {
    p *= -1
  }
}
