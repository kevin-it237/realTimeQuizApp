axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

// When the admin launch the quiz
redirectToQuiz = () => {
    axios({
      method: "POST",
      url: "/check_when_redirect/",
      headers: {
        "content-type": "application/json"
      }
    })
      .then(function(response) {
        if (response.data == 'False') {
            window.location.href = '/';
        }
      })
      .catch(function(error) {

      });
};

redirectToQuiz()

setInterval(function() {
    redirectToQuiz();
}, 5000)