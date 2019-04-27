axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

// This function get the results in the database
const resultBloc = document.querySelector(".dashboard_container");
getRealTimeResults = () => {
    axios({
        method: "POST",
        url: "/dashboard/",
        headers: {
        "content-type": "application/json"
        }
    })
    .then(function(response) {
        $(".dashboard_container").html(renderResults(response.data.data));
        if (response.data.is_stopped) {
            const html = `<button id="start">Start Quiz</button>`;
            $(".controls").html(html);
            // have event listener to button start button
            addListenerToStartBtn();
        } else {
            const html = `<button id="stop">Stop Quiz</button>`;
            $(".controls").html(html);
            // have event listener to button start button
            addListenerToStopBtn();
        }
    })
    .catch(function(error) {
      alert(error);
    });
};

getRealTimeResults();

// Get new datas after a few seconds
setInterval(function() {
  getRealTimeResults();
}, 2000);

// Get and format data from API
renderResults = data => {
  let html = `<div class="result result__header">
                <div class="rang"><span>Rang</span></div>
                <div class="name"><span>Nom</span></div>
                <div class="email"><span>Adresse Email</span></div>
                <div class="marks"><span>Score</span></div>
                <div class="progression"><span>Progression</span></div>
            </div>`;
  data.forEach(result => {
    let rang = ``;
    if (result.n == 1) {
      rang = `<img class="medail" src="../static/imgs/1.png" alt="Or">`;
    }
    if (result.n == 2) {
      rang = `<img class="medail" src="../static/imgs/2.png" alt="Or">`;
    }
    if (result.n == 3) {
      rang = `<img class="medail" src="../static/imgs/3.png" alt="Or">`;
    }
    if (result.n > 3) {
      rang = `<span>${result.n}</span>`;
    }
    html += `<div class="result">
                <div class="rang">
                    ${rang}
                </div>
                <div class="name"><span>${result.name}</span></div>
                <div class="email"><span>${result.email}</span></div>
                <div class="marks"><span>${result.score}</span></div>
                <div class="progression">
                    <div class="progress">
                        <div class="progress-bar bg-dark" style="width:${
                            result.questions
                        }%"></div>
                    </div>
                </div>
            </div>`;
  });
  return html;
};

stopOrStartQuiz = (value) => {
    axios({
      method: "POST",
      url: "/stop_quiz/",
      data: {
        haveStopped: value
      },
      headers: {
        "content-type": "application/json"
      }
    })
      .then(function(response) {
        getRealTimeResults();
      })
      .catch(function(error) {
        alert(error);
      });
};

addListenerToStopBtn = () => {
    const stopBtn = document.querySelector("#stop");
    stopBtn.addEventListener("click",function() {
        let loader = '<i class="fas fa-spinner fa-1x fa-spin"></i>';
        stopBtn.innerHTML = loader;
        stopOrStartQuiz(true);
    });
}


addListenerToStartBtn = () => {
    const startBtn = document.querySelector("#start");
    startBtn.addEventListener("click", function() {
        let loader = '<i class="fas fa-spinner fa-1x fa-spin"></i>';
        startBtn.innerHTML = loader;
        stopOrStartQuiz(false);
    });
}
