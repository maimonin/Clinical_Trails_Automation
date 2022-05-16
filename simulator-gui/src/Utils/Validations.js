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

export const isValidAnswersSet = (answers) => {
    return true;
        //TODO : chheck empty_singlechoice_answer
    //answers.every(element => (typeof element === "string" && element != "") | 
    
}