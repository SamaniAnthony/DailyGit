//I am going to export a class in file because the engine has state(or rules), and we create instances of it. 
console.log("engine.js loaded")

class RulesEngine {
    receiveForm(ourForm) {
        console.log("Engine received:", ourForm)

        return {status: "received", data: ourForm}
    }
}
module.exports = RulesEngine

