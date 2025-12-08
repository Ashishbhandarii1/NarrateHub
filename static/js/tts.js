document.addEventListener('DOMContentLoaded', function() {
    const playBtn = document.getElementById('tts-play');
    const pauseBtn = document.getElementById('tts-pause');
    const stopBtn = document.getElementById('tts-stop');
    const voiceSelect = document.getElementById('voice-select');
    const contentTextRaw = document.getElementById('content-text-raw');
    const contentLanguage = document.getElementById('content-language')?.value || 'English';

    if (!playBtn || !contentTextRaw) return;

    let utterance = null;
    let isPaused = false;
    let voices = [];
    let voicesLoaded = false;
    let selectedVoice = null;

    const languageCodeMap = {
        'English': ['en', 'en-US', 'en-GB', 'en-AU', 'en-IN'],
        'Spanish': ['es', 'es-ES', 'es-MX', 'es-US'],
        'French': ['fr', 'fr-FR', 'fr-CA'],
        'German': ['de', 'de-DE'],
        'Italian': ['it', 'it-IT'],
        'Portuguese': ['pt', 'pt-BR', 'pt-PT'],
        'Russian': ['ru', 'ru-RU'],
        'Japanese': ['ja', 'ja-JP'],
        'Korean': ['ko', 'ko-KR'],
        'Chinese': ['zh', 'zh-CN', 'zh-TW', 'zh-HK'],
        'Arabic': ['ar', 'ar-SA'],
        'Hindi': ['hi', 'hi-IN'],
        'Dutch': ['nl', 'nl-NL'],
        'Polish': ['pl', 'pl-PL'],
        'Turkish': ['tr', 'tr-TR'],
        'Swedish': ['sv', 'sv-SE'],
        'Norwegian': ['no', 'nb', 'nb-NO'],
        'Danish': ['da', 'da-DK'],
        'Finnish': ['fi', 'fi-FI']
    };

    const femaleKeywords = ['female', 'woman', 'girl', 'samantha', 'victoria', 'karen', 'moira', 'tessa', 'fiona', 'veena', 'zira', 'susan', 'hazel', 'heera', 'allison', 'ava', 'nicky', 'siri'];
    const maleKeywords = ['male', 'man', 'boy', 'david', 'james', 'daniel', 'alex', 'tom', 'fred', 'ralph'];

    function loadVoices() {
        voices = speechSynthesis.getVoices();
        if (voices.length > 0) {
            voicesLoaded = true;
            populateVoiceSelector();
        }
    }

    function populateVoiceSelector() {
        if (!voiceSelect) return;
        
        voiceSelect.innerHTML = '<option value="">Auto (Best Match)</option>';
        
        const langCodes = languageCodeMap[contentLanguage] || ['en'];
        const matchingVoices = voices.filter(v => 
            langCodes.some(code => v.lang.toLowerCase().startsWith(code.toLowerCase()))
        );
        
        if (matchingVoices.length > 0) {
            const optgroup = document.createElement('optgroup');
            optgroup.label = `${contentLanguage} Voices`;
            
            matchingVoices.forEach(voice => {
                const option = document.createElement('option');
                option.value = voice.name;
                const gender = isFemaleVoice(voice) ? '♀' : (isMaleVoice(voice) ? '♂' : '');
                option.textContent = `${gender} ${voice.name}`;
                optgroup.appendChild(option);
            });
            
            voiceSelect.appendChild(optgroup);
        }
        
        const otherVoices = voices.filter(v => 
            !langCodes.some(code => v.lang.toLowerCase().startsWith(code.toLowerCase()))
        );
        
        if (otherVoices.length > 0) {
            const optgroup = document.createElement('optgroup');
            optgroup.label = 'Other Languages';
            
            otherVoices.forEach(voice => {
                const option = document.createElement('option');
                option.value = voice.name;
                option.textContent = `${voice.name} (${voice.lang})`;
                optgroup.appendChild(option);
            });
            
            voiceSelect.appendChild(optgroup);
        }
    }

    function isFemaleVoice(voice) {
        const nameLower = voice.name.toLowerCase();
        return femaleKeywords.some(keyword => nameLower.includes(keyword));
    }

    function isMaleVoice(voice) {
        const nameLower = voice.name.toLowerCase();
        return maleKeywords.some(keyword => nameLower.includes(keyword));
    }

    function getBestVoiceForLanguage(lang) {
        const langCodes = languageCodeMap[lang] || ['en'];
        
        const matchingVoices = voices.filter(v => 
            langCodes.some(code => v.lang.toLowerCase().startsWith(code.toLowerCase()))
        );
        
        if (matchingVoices.length > 0) {
            const femaleVoices = matchingVoices.filter(isFemaleVoice);
            if (femaleVoices.length > 0) {
                return femaleVoices[0];
            }
            
            const nonMaleVoices = matchingVoices.filter(v => !isMaleVoice(v));
            if (nonMaleVoices.length > 0) {
                return nonMaleVoices[0];
            }
            
            return matchingVoices[0];
        }
        
        const femaleVoices = voices.filter(isFemaleVoice);
        if (femaleVoices.length > 0) {
            return femaleVoices[0];
        }
        
        return voices[0] || null;
    }

    loadVoices();
    if (speechSynthesis.onvoiceschanged !== undefined) {
        speechSynthesis.onvoiceschanged = loadVoices;
    }
    setTimeout(loadVoices, 100);
    setTimeout(loadVoices, 500);

    if (voiceSelect) {
        voiceSelect.addEventListener('change', function() {
            const selectedName = this.value;
            if (selectedName) {
                selectedVoice = voices.find(v => v.name === selectedName);
            } else {
                selectedVoice = null;
            }
        });
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
        
        if (selectedVoice) {
            utterance.voice = selectedVoice;
        } else {
            const bestVoice = getBestVoiceForLanguage(contentLanguage);
            if (bestVoice) {
                utterance.voice = bestVoice;
            }
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
