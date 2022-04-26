export const isValidUserData = (userDetails) =>
{
return (
isNotEmptyString(userDetails.name)  && isNotEmptyString(userDetails.sex) &&
 isNumericString(userDetails.age) && isNumericString(userDetails.id) && isNotEmptyString(userDetails.role))




}

const isString = (value) => typeof(value) ==="string"
const isNumericString = (value) => isString(value) && !isNaN(+value)
const isNotEmptyString = (value) => isString(value) & value !== ""