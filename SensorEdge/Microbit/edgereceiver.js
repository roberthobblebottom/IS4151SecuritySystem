let globalalarm = 3
let forcedalarm = 5
let motion = 0
let state = -1
let x = input.acceleration(Dimension.X)
let y = input.acceleration(Dimension.Y)
let z = input.acceleration(Dimension.Z)

radio.onReceivedValue(function (name, value) {
    if (name == "int" && state == 0) {
        serial.writeLine(radio.receivedPacket(RadioPacketProperty.SerialNumber) + " " + name + " " + value)
        music.playTone(Note.C, music.beat())
    } else if (name == "awake") {
        if (state == 1) {
            radio.sendValue("unarm", 1)
        } else if (state == 0) {
            radio.sendValue("arm", 0)
        }
        basic.pause(50)
        radio.sendValue("gad", globalalarm)
        basic.pause(50)
        radio.sendValue("fad", forcedalarm)
        basic.pause(50)
        radio.sendValue("motion", motion)
    }
})

serial.onDataReceived(serial.delimiters(Delimiters.NewLine), function () {
    let msg = serial.readUntil(serial.delimiters(Delimiters.NewLine))
    let list = msg.split("$")
    if (list[0] == "unarm") {
        state = 1
        radio.sendValue("unarm", 1)
        music.playTone(Note.C, music.beat())
    } else if (list[0] == "arm") {
        state = 0
        radio.sendValue("arm", 0)
        music.playTone(Note.G, music.beat())
    } else if (list[0] == "alarm") {
        radio.sendValue("alarm", 0)
    } else if (list[0] == "shutdown") {
        state = -1
        radio.sendValue("shutdown", -1)
    } else if (list[0] == "gad") {
        globalalarm = parseInt(list[1])
        radio.sendValue("gad", globalalarm)
    } else if (list[0] == "fad") {
        forcedalarm = parseInt(list[1])
        radio.sendValue("fad", forcedalarm)
    } else if (list[0] == "md") {
        let tempMotion = parseInt(list[1])
        if (motion == 1) {
            x = input.acceleration(Dimension.X)
            y = input.acceleration(Dimension.Y)
            z = input.acceleration(Dimension.Z)
        }
        basic.pause(200)
        motion = tempMotion
        radio.sendValue("motion", motion)
    }
})

radio.setGroup(69)
radio.setTransmitPower(7)
radio.setFrequencyBand(7)
radio.setTransmitSerialNumber(true)
serial.redirectToUSB()

basic.forever(function () {
	if (motion == 1) {
         if (Math.abs(x - input.acceleration(Dimension.X)) > 100 || 
            Math.abs(y - input.acceleration(Dimension.Y)) > 100 || 
            Math.abs(z - input.acceleration(Dimension.Z)) > 100) {
                serial.writeLine(control.deviceSerialNumber() + " " + "int" + " 0")
                music.playTone(Note.C, music.beat())
                x = input.acceleration(Dimension.X)
                y = input.acceleration(Dimension.Y)
                z = input.acceleration(Dimension.Z)
                basic.pause(10000)
            }
    }
})
