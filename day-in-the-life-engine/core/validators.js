//I will export a function here because validation is a stateless operation and you just call it. 
console.log("validators.js loaded")

function validate(ourForm) {
    console.log("got the form");
    return ourForm;   
}

module.exports = { validate }

