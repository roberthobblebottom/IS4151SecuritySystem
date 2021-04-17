let distance = 999
let state = -1
radio.setGroup(69)
radio.setTransmitPower(7)
radio.setFrequencyBand(7)
radio.setTransmitSerialNumber(true)
let globalalarm = 3
let forcedalarm = 5
let motion = 0
basic.pause(1000)
let x = input.acceleration(Dimension.X)
let y = input.acceleration(Dimension.Y)
let z = input.acceleration(Dimension.Z)

input.onButtonPressed(Button.AB, function () {
    radio.sendValue("awake", 0);
})


radio.onReceivedValue(function (name: string, value: number) {
    if (name == "arm") {
        state = 0
        music.playTone(Note.C5, music.beat())
    } else if (name == "unarm") {
        state = 1
        music.playTone(Note.C, music.beat())
    } else if (name == "alarm") {
        music.playTone(Note.C, forcedalarm * 1000)
    } else if (name == "shutdown") {
        state = -1
        music.playTone(Note.C4, music.beat())
        basic.clearScreen()
    } else if (name == "gad") {
        globalalarm = value
    } else if (name == "fad") {
        forcedalarm = value
    } else if (name == "motion") {
        if (value == 1) {
            x = input.acceleration(Dimension.X)
            y = input.acceleration(Dimension.Y)
            z = input.acceleration(Dimension.Z)
        }
        basic.pause(1000)
        motion = value
    }
})

function showAlarm() {
    basic.showLeds(`
        # . . . #
        . # . # .
        . . # . .
        . . # . .
        . # . # .
    `)
    radio.sendValue("int", 0)
    x = input.acceleration(Dimension.X)
    y = input.acceleration(Dimension.Y)
    z = input.acceleration(Dimension.Z)
    music.playTone(Note.G4, globalalarm * 1000)
    basic.pause(10000)
    basic.clearScreen()
}

basic.forever(function () {
    if (state == 0) {
        distance = grove.measureInCentimeters(DigitalPin.P2)
        if (distance <= 30) {
            showAlarm()
        } else if (motion == 1) {
            if (Math.abs(x - input.acceleration(Dimension.X)) > 50 || 
            Math.abs(y - input.acceleration(Dimension.Y)) > 50 || 
            Math.abs(z - input.acceleration(Dimension.Z)) > 50) {
                showAlarm()
            }
        }
    }
})
