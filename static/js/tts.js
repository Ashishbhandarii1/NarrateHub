document.addEventListener('DOMContentLoaded', function() {
    const playBtn = document.getElementById('tts-play');
    const pauseBtn = document.getElementById('tts-pause');
    const stopBtn = document.getElementById('tts-stop');
    const contentTextRaw = document.getElementById('content-text-raw');

    if (!playBtn || !contentTextRaw) return;

    let utterance = null;
    let isPaused = false;
    let voices = [];
    let voicesLoaded = false;

    function loadVoices() {
        voices = speechSynthesis.getVoices();
        if (voices.length > 0) {
            voicesLoaded = true;
        }
    }

    loadVoices();
    if (speechSynthesis.onvoiceschanged !== undefined) {
        speechSynthesis.onvoiceschanged = loadVoices;
    }
    
    setTimeout(loadVoices, 100);
    setTimeout(loadVoices, 500);

    function getFemaleVoice() {
        const femaleKeywords = ['female', 'woman', 'girl', 'samantha', 'victoria', 'karen', 'moira', 'tessa', 'fiona', 'veena', 'zira', 'susan', 'hazel', 'heera'];
        
        for (let voice of voices) {
            const nameLower = voice.name.toLowerCase();
            for (let keyword of femaleKeywords) {
                if (nameLower.includes(keyword)) {
                    return voice;
                }
            }
        }

        const englishVoices = voices.filter(v => v.lang.startsWith('en'));
        if (englishVoices.length > 0) {
            for (let voice of englishVoices) {
                if (!voice.name.toLowerCase().includes('male') && 
                    !voice.name.toLowerCase().includes('david') &&
                    !voice.name.toLowerCase().includes('james') &&
                    !voice.name.toLowerCase().includes('daniel')) {
                    return voice;
                }
            }
            return englishVoices[0];
        }

        return voices[0] || null;
    }

    function updateButtonStates(state) {
        switch(state) {
            case 'idle':
                playBtn.disabled = false;
                playBtn.innerHTML = '<span class="tts-icon">&#9658;</span> Play';
                playBtn.classList.remove('active');
                pauseBtn.disabled = true;
                pauseBtn.innerHTML = '<span class="tts-icon">&#10074;&#10074;</span> Pause';
                stopBtn.disabled = true;
                break;
            case 'playing':
                playBtn.disabled = true;
                playBtn.innerHTML = '<span class="tts-icon">&#9658;</span> Playing...';
                playBtn.classList.add('active');
                pauseBtn.disabled = false;
                pauseBtn.innerHTML = '<span class="tts-icon">&#10074;&#10074;</span> Pause';
                stopBtn.disabled = false;
                break;
            case 'paused':
                playBtn.disabled = true;
                pauseBtn.disabled = false;
                pauseBtn.innerHTML = '<span class="tts-icon">&#9658;</span> Resume';
                stopBtn.disabled = false;
                break;
        }
    }

    function speak() {
        if (speechSynthesis.speaking) {
            speechSynthesis.cancel();
        }

        if (!voicesLoaded) {
            loadVoices();
        }

        const text = contentTextRaw.textContent.trim();
        if (!text) return;

        utterance = new SpeechSynthesisUtterance(text);
        
        const femaleVoice = getFemaleVoice();
        if (femaleVoice) {
            utterance.voice = femaleVoice;
        }

        utterance.rate = 0.9;
        utterance.pitch = 1.1;

        utterance.onstart = function() {
            updateButtonStates('playing');
        };

        utterance.onend = function() {
            updateButtonStates('idle');
            isPaused = false;
        };

        utterance.onerror = function(event) {
            if (event.error !== 'canceled') {
                console.error('Speech synthesis error:', event.error);
            }
            updateButtonStates('idle');
            isPaused = false;
        };

        speechSynthesis.speak(utterance);
    }

    playBtn.addEventListener('click', function() {
        speak();
    });

    pauseBtn.addEventListener('click', function() {
        if (speechSynthesis.speaking) {
            if (isPaused) {
                speechSynthesis.resume();
                isPaused = false;
                updateButtonStates('playing');
            } else {
                speechSynthesis.pause();
                isPaused = true;
                updateButtonStates('paused');
            }
        }
    });

    stopBtn.addEventListener('click', function() {
        speechSynthesis.cancel();
        isPaused = false;
        updateButtonStates('idle');
    });

    window.addEventListener('beforeunload', function() {
        if (speechSynthesis.speaking) {
            speechSynthesis.cancel();
        }
    });
});
