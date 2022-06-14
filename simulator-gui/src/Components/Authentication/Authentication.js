import React, { useState, useEffect } from "react";
import Box from '@mui/material/Box';
import Input from '@mui/material/Input';
import Button from '@mui/material/Button';
import { blankUser } from "../UserWindow/UserWindow";
import {isValidRegisterUserData} from '../../Utils/Validations'
import ShortuctsMenu from '../Shortcuts/Shortcuts'
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import { toast } from "react-toastify";

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
    
    const row_style = {width:200}
    const handle_send = () => {
        if(isValidRegisterUserData(userDetails)){
          props.sendRegister(userDetails)
        }
        else{
          // console.log(props.containerId)
          // toast("Invalid details",{"containerId":props.containerId, toastId:"wrong details"})
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
  const get_user_and_send = (user)=>{
    props.sendRegister(user)
  }
    return (<>
    <ShortuctsMenu set_user = {get_user_and_send} />
       <Box
      component="form"
      sx={{
        '& > :not(style)': { m: 1 },
        marginTop:"10px"
      }}
      noValidate
      autoComplete="off"
    >
      Please enter the following:
      <Input name="name" placeholder="Name" onChange={set_value} inputProps={ariaLabel} />
      <Autocomplete name="role"
        onChange={(event,newValue)=>setUserDetails((prev)=>({ ...prev,"role": newValue }))}
        id="controllable-states-demo"
        options={["doctor" ,"nurse","lab technician", "investigator", "participant",]}
        sx={row_style}
        renderInput={(params) => <TextField {...params} label="Role" sx={{ marginLeft:"30px"}}/>}
      />

      <Autocomplete name="sex"
        onChange={(event,newValue)=>setUserDetails((prev)=>({ ...prev,"sex": newValue }))}
        id="controllable-states-demo"
        options={["male","female"]}
        sx={row_style}
        renderInput={(params) => <TextField {...params} label="sex" sx={{ marginLeft:"30px"}}/>}
      />      
      
      <Input sx={row_style} name ="age" placeholder="Age" onChange={set_integer} inputProps={ariaLabel} />
      <Input sx={row_style} name="id" placeholder="ID" onChange={set_integer} inputProps={ariaLabel} />
      <Button sx={row_style} onClick={handle_send}>Register</Button>
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
