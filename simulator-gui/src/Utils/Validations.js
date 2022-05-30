import { element } from "prop-types";
import { empty_singlechoice_answer } from "../Components/Question/Question";

export const isValidRegisterUserData = (userDetails) =>
{
return (
isNotEmptyString(userDetails.name)  && isNotEmptyString(userDetails.sex) &&
 greaterThanZero(userDetails.age) && greaterThanZero(userDetails.id) && isNotEmptyString(userDetails.role))
}
export const isValidLoginUserData = (userDetails) =>
{
return (
isNotEmptyString(userDetails.name)  && isNotEmptyString(userDetails.sex) &&
 greaterThanZero(userDetails.age) && greaterThanZero(userDetails.id) && isNotEmptyString(userDetails.role))
}

const isString = (value) =>typeof(value) ==="string"
const greaterThanZero = (value) => value>0
const isNotEmptyString = (value) => isString(value) & value !== ""

export const isValidAnswersToQuestionnaire = (answers) =>{


}

export const isValidAnswersSet = (questions,answers) => {
    console.log(questions + "~~~" + answers)

    for (let i =0; i<answers.length; i++){
        if (questions[i]["type"] ===  "one choice" && answers[i] ==="")
       { console.log(questions[i] + ";;;i is " + i +";;;" + answers[i])
        return false
    }
    }
    return true;
        
    
}