import Questionnaire from "../Components/Question/Question";

export const getComponent = (itemToAdd,callback) => {
    // return (<TestNotification test={1}/>)
    switch(itemToAdd["type"]) {
      case "questionnaire":

        return (<Questionnaire questionnaire = {itemToAdd} send ={callback}/>)
          case "":
        break;
      default:
        console.log("SubWindow::getComponent::default block ~ ")

        // code block
    } 
    // <TestQuestionnaire/>  //change to switch case, and parse json accordingly

  }

  export const isComponent = (message) => {
    const valid_types = ["questionnaire",]  
    

      return valid_types.includes(message["type"])
  }