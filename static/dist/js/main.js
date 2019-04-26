axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

const form = document.getElementById("responseForm");
const submitBtn = document.getElementById("submit");

sendResponse = () => {
    let rep = [];
    //J'initialise le tableau avec les valeurs cochées
    $("input[name='rep']:checked").each(function() {
        rep.push(this.value);
    });
    // Get the question Id
    let questionId = document.getElementById("questionId").value;

    axios({
        method: "POST",
        url: "/",
        data: {
            response: rep,
            questionId: questionId
        },
        headers: {
            "content-type": "application/json"
        }
    })
    .then(function(response) {
        window.location.href = '/'; 
    })
    .catch(function(error) {
        clearLoader();
        alert(error);
    });
}

$("#responseForm").submit(function(e) {
    // Let render the loader
    renderLoader();
    sendResponse();
    return false;
})

renderLoader = () => {
    let loader = '<i class="fas fa-spinner fa-3x fa-spin"></i>';
    submitBtn.innerHTML = loader;
}

clearLoader = () => {
    submitBtn.innerHTML = "<span>Valider</span>";
}


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
        alert(response)
        window.location.href = "/";
        resultBloc.insertAdjacentElement('beforeend', "<h1>jojo</h1>")
    })
    .catch(function(error) {
        alert(error);
    });
}

getRealTimeResults();

// Get new datas after a few seconds
setInterval(() => {
    getRealTimeResults();
}, 1000)