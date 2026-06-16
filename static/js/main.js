document.getElementById('run-btn').onclick = async () => {
    const url = document.getElementById('target-url').value;
    const username = document.getElementById('target-user').value;
    const wordlist = document.getElementById('wordlist').value;
    const log = document.getElementById('log-window');
    const banner = document.getElementById('found-banner');
    const status = document.getElementById('status-display');

    if(!username || !wordlist) {
        alert("CRITICAL: Username and Wordlist required.");
        return;
    }

    // Reset UI
    status.classList.remove('hidden');
    banner.classList.add('hidden');
    log.innerHTML = "INITIATING ATTACK SEQUENCE...<br>";

    try {
        const response = await fetch('/start_attack', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ url, username, wordlist })
        });

        const data = await response.json();

        if (!data.success) {
            log.innerHTML += `<span style="color:red;">[ERR] ${data.message}</span>`;
            return;
        }

        log.innerHTML = "";
        data.attempts.forEach(attempt => {
            const p = document.createElement('p');
            p.style.margin = "0";
            p.innerText = `[-] PASSWORD: ${attempt.password} | STATUS: ${attempt.status}`;
            if(attempt.status === "SUCCESS") p.style.color = "white";
            log.appendChild(p);
        });

        if(data.found) {
            banner.classList.remove('hidden');
            document.getElementById('cracked-pw').innerText = data.found;
        }

        const logInfo = document.createElement('p');
        logInfo.style.color = "#888";
        logInfo.style.marginTop = "15px";
        logInfo.innerText = `[INFO] Audit log generated at: ${data.log_file}`;
        log.appendChild(logInfo);
        
        log.scrollTop = log.scrollHeight;

    } catch (err) {
        log.innerHTML += `<span style="color:red;"><br>[ERR] CONNECTION TO ATTACK ENGINE LOST.</span>`;
    }
};