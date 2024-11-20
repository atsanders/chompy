import QtQuick 
import QtQuick.Controls
import QtQuick.Dialogs

ApplicationWindow {
    visible: true
    width: 400
    height: 200
    title: "File Selector"

    FileDialog {
        id: fileDialog
        title: "Select a File"
        onAccepted: {
            console.log("Selected file: " + fileDialog.file)
        }
        onRejected: {
            console.log("File selection canceled")
        }
    }

    Column {
        anchors.centerIn: parent
        spacing: 10

        Text {
            id: selectedFileLabel
            text: "No file selected"
            horizontalAlignment: Text.AlignHCenter
        }

        Button {
            text: "Select File"
            onClicked: fileDialog.open()
        }
    }
}
