$(document).ready(function () {
    $('.text').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "bounceIn",
        },
        out:{
            effect: "bounceOut",
        },
    });

    // Siri configuration
 var siriWave = new SiriWave({
    container: document.getElementById("siri-container"),
    width: 850,
    height: 200,
    style:"ios9",
    apmlitude: "1.5",
    speed:"0.35",
    autostar: true
  });

//   Siri Message Animation
$('.SiriMessage').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "fadeInUp",
            sync:true
        },
        out:{
            effect: "fadeOutUp",
            sync:true
        },
    });

    // Mic Button Click Event
    $("#micbutton").click(function () {

        eel.PlayAssistSound()
        $("#Oval").attr("hidden", true);
        $("#SiriWave").attr("hidden", false);
        eel.allCommands()()
        
    });

    function doc_keyUp(e) {
        // this would test for whichever key is 40 (down arrow) and the ctrl key at the same time

        if (e.key === 'j' && e.metaKey) {
            eel.PlayAssistSound()
            $("#Oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.allCommands()()
        }
    }
    document.addEventListener('keyup', doc_keyUp, false);

    function PlayAssistant(message) {

        if (message != "") {

            $("#Oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.allCommands(message);
            $("#chatbox").val("")
            $("#micbutton").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);

        }
    }

    // toogle fucntion to hide and display mic and send button 
    function ShowHideButton(message) {
        if (message.length == 0) {
            $("#micbutton").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);
        }
        else {
            $("#micbutton").attr('hidden', true);
            $("#SendBtn").attr('hidden', false);
        }
    }


    // key up event handler on text box
    $("#chatbox").keyup(function () {

        let message = $("#chatbox").val();
        ShowHideButton(message)

    });

    // send button event handler
    $("#SendBtn").click(function () {

        let message = $("#chatbox").val()
        PlayAssistant(message)

    });

    // enter press event handler on chat box
    $("#chatbox").keypress(function (e) {
        key = e.which;
        if (key == 13) {
            let message = $("#chatbox").val()
            PlayAssistant(message)
        }
    });

});