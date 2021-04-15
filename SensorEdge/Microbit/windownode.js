let distance = 999
let state = -1
radio.setGroup(69)
radio.setTransmitPower(7)
radio.setFrequencyBand(7)
radio.setTransmitSerialNumber(true)

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
        music.playTone(Note.C, 5000)
    } else if (name == "shutdown") {
        state = -1
        music.playTone(Note.C4, music.beat())
        basic.clearScreen()
    }
})

basic.forever(function () {
    distance = grove.measureInCentimeters(DigitalPin.P2)
    if (distance <= 30) {
        if (state == 0) {
            basic.showLeds(`
            # . . . #
            . # . # .
            . . # . .
            . . # . .
            . # . # .
            `)
            music.playTone(Note.G4,music.beat())
            radio.sendValue("int", 0)
            basic.pause(10000)
            basic.clearScreen()
        }
    }
})
