$(document).ready(function() {
    const url = window.location.href;
    const quizBox = document.getElementById('quiz-box');
    const timerBox = document.getElementById('timer-box');
    let timer; // Timer variable

    const activateTimer = (time) => {
        // First state
        if (time.toString().length < 2) {
            timerBox.innerHTML = `<b>0${time}:00</b>`;
        } else {
            timerBox.innerHTML = `<b>${time}:00</b>`;
        }

        // Countdown
        let minutes = time - 1;
        let seconds = 60;
        let displaySeconds;
        let displayMinutes;

        timer = setInterval(() => {
            seconds--;
            if (seconds < 0) {
                seconds = 59;
                minutes--;
            }
            if (minutes.toString().length < 2) {
                displayMinutes = '0' + minutes;
            } else {
                displayMinutes = minutes;
            }

            if (seconds.toString().length < 2) {
                displaySeconds = '0' + seconds;
            } else {
                displaySeconds = seconds;
            }

            if (minutes === 0 && seconds === 0) {
                timerBox.innerHTML = '<b>00:00</b>';
                setTimeout(() => {
                    clearInterval(timer);
                    Swal.fire({
                        icon: 'warning',
                        title: 'Vaqt tugadi!',
                        text: 'Viktorina vaqti tugadi. Javoblaringiz avtomatik ravishda yuboriladi.',
                        confirmButtonText: 'OK'
                    }).then((result) => {
                        if (result.isConfirmed) {
                            sendData();
                        }
                    });
                }, 500);
            }
            console.log(displayMinutes, displaySeconds);
            timerBox.innerHTML = `<b>${displayMinutes}:${displaySeconds}</b>`;
        }, 1000);
    };

    $.ajax({
        type: 'GET',
        url: `${url}data`, // Gets data from JsonResponse
        success: function(response) {
            const data = response.data;
            const time = response.time;
            data.forEach(element => { // A dictionary of a Question and its answers
                for (const [question, answers] of Object.entries(element)) {
                    quizBox.innerHTML += `
                        <hr>
                        <div class="quiz-question">
                            <b>${question}</b>
                        </div>
                    `;
                    answers.forEach(answer => {
                        quizBox.innerHTML += `
                            <div class="quiz-answer">
                                <input type="radio" class="ans" id="${question}-${answer}" name="${question}" value="${answer}">
                                <label for="${question}">${answer}</label>
                            </div>
                        `;
                    });
                }
            });
            activateTimer(time);
        },
        error: function(error) {
            console.log(error);
        }
    });

    const quizForm = document.getElementById('quiz-form');
    const csrf = document.getElementsByName('csrfmiddlewaretoken');
    const scoreBox = document.getElementById('score-box');
    const resultBox = document.getElementById('result-box');

    const sendData = () => {
        clearInterval(timer); // Stops the timer
        timerBox.remove(); // Removes the timer display

        const elements = [...document.getElementsByClassName('ans')];
        const data = {};
        data['csrfmiddlewaretoken'] = csrf[0].value;
        elements.forEach(el => {
            if (el.checked) {
                data[el.name] = el.value;
            } else {
                if (!data[el.name]) {
                    data[el.name] = null;
                }
            }
        });

        $.ajax({
            type: 'POST',
            url: `${url}save`,
            data: data,
            success: function(response) {
                const results = response.results;
                const n_correct_answers = response.correct_questions;
                const score = response.score.toFixed(2);
                const passed = response.passed;

                // Removes the form 
                quizForm.remove();

                let scoreDiv = document.createElement('div');
                scoreDiv.innerHTML += `
                    <div class="${passed ? 'result-success' : 'result-failure'}">
                        ${passed ? '<i class="fa-regular fa-face-smile"></i> Tabriklaymiz, siz sinovdan o\'tdingiz!' : '<i class="fa-regular fa-face-smile"></i> Kechirasiz, siz testdan o\'ta olmadingiz!'} Sizning natijangiz ${score}%.
                        <br><i class="fa-solid fa-check"></i> To'g'ri javoblar soni: ${n_correct_answers}
                    </div>
                `;

                scoreBox.append(scoreDiv);

                results.forEach(res => {
                    let resDiv = document.createElement('div');

                    for (const [question, resp] of Object.entries(res)) {
                        resDiv.innerHTML += `<b>${question}</b><br>`;

                        if (resp == 'not answered') {
                            resDiv.classList.add('not-answered');
                            resDiv.innerHTML += '<i class="fa-solid fa-exclamation"></i> Javob berilmagan';
                        } else {
                            const answer = resp['answered'];
                            const correct = resp['correct_answer'];

                            if (answer == correct) {
                                resDiv.classList.add('result-success');
                                resDiv.innerHTML += `<i class="fa-solid fa-check"></i> Sizning javobingiz: ${answer}`;
                            } else {
                                resDiv.classList.add('result-failure');
                                resDiv.innerHTML += `<i class="fa-solid fa-xmark"></i> Sizning javobingiz: ${answer}<br><i class="fa-solid fa-check"></i> To'g'ri javob: ${correct}`;
                            }
                        }
                    }
                    resultBox.append(resDiv);
                });
            },
            error: function(error) {
                console.log(error);
            }
        });
    };

    quizForm.addEventListener('submit', element => {
        element.preventDefault();
        sendData();
    });
});
