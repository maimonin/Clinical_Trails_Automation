import { element } from "prop-types";
import { empty_singlechoice_answer } from "../Components/Question/Question";

export const isValidUserData = (userDetails) =>
{
return (
isNotEmptyString(userDetails.name)  && isNotEmptyString(userDetails.sex) &&
 isNumericString(userDetails.age) && isNumericString(userDetails.id) && isNotEmptyString(userDetails.role))
}

const isString = (value) => typeof(value) ==="string"
const isNumericString = (value) => isString(value) && !isNaN(+value)
const isNotEmptyString = (value) => isString(value) & value !== ""

export const isValidAnswersToQuestionnaire = (answers) =>{


}

export const isValidAnswersSet = (answers) => {
    return true;
        //TODO : chheck empty_singlechoice_answer
    //answers.every(element => (typeof element === "string" && element != "") | 
    
}