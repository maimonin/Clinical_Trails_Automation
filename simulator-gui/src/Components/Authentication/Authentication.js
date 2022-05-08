import React, { useState, useEffect } from "react";
import Box from '@mui/material/Box';
import Input from '@mui/material/Input';
import Button from '@mui/material/Button';
import { blankUser } from "../UserWindow/UserWindow";
import {isValidRegisterUserData} from '../../Utils/Validations'


const ariaLabel = { 'aria-label': 'description' };

function Authentication(props){
    const isRegister = ()=> props.toggleRegister
    return (
        <div>
    {
        isRegister()? <RegisterScreen sendRegister={props.sendRegister}/> : <LoginScreen sendLogin={props.sendLogin}/>
    }
</div>

    )
}
export function RegisterScreen(props){
    const [userDetails,setUserDetails] = useState(blankUser)
    
    const handle_send = () => {
        if(isValidRegisterUserData(userDetails)){
          props.sendRegister(userDetails)
        }
    }
    const set_value = (e) =>{
        const value = e.target.value;   
        setUserDetails((prev)=>({ ...prev,[e.target.name]: value }));
    }
    const set_integer = (e) =>{
      const value = parseInt(e.target.value);   
      setUserDetails((prev)=>({ ...prev,[e.target.name]: value }));
  }
    return (<>
       <Box
      component="form"
      sx={{
        '& > :not(style)': { m: 1 },
      }}
      noValidate
      autoComplete="off"
    >

      <Input name="name" placeholder="Name" onChange={set_value} inputProps={ariaLabel} />
      <Input name="role" placeholder="Role" onChange={set_value} inputProps={ariaLabel} />
      <Input name="sex" placeholder="Sex" onChange={set_value} inputProps={ariaLabel} />
      <Input name ="age" placeholder="Age" onChange={set_integer} inputProps={ariaLabel} />
      <Input name="id" placeholder="ID" onChange={set_integer} inputProps={ariaLabel} />
      <Button onClick={handle_send}>Register</Button>
    </Box></>)
}
function LoginScreen(props){
    const [userDetails,setUserDetails] = useState(blankUser)
    
    const handle_send = () => {
        if(isValidRegisterUserData(userDetails)){
          props.sendLogin(userDetails)
        }
    }

    const set_integer = (e) =>{
      const value = parseInt(e.target.value);   
      setUserDetails((prev)=>({ ...prev,[e.target.name]: value }));
  }
    return (<>
       <Box
      component="form"
      sx={{
        '& > :not(style)': { m: 1 },
      }}
      noValidate
      autoComplete="off"
    >

      <Input name="id" placeholder="ID" onChange={set_integer} inputProps={ariaLabel} />
      <Button onClick={handle_send}>Login</Button>
    </Box></>)
}


export default Authentication;
