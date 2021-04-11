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
    }
})

radio.setGroup(69)
radio.setTransmitPower(7)
radio.setFrequencyBand(7)
radio.setTransmitSerialNumber(true)
serial.redirectToUSB()
let state = 0
basic.forever(function () {
	
})
