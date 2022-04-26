import React, { useState } from "react";
import Box from '@mui/material/Box';
import Input from '@mui/material/Input';
import Button from '@mui/material/Button';
import { blankUser } from "../UserWindow/UserWindow";
import {isValidUserData} from '../../Utils/Validations'


const ariaLabel = { 'aria-label': 'description' };
function RegisterScreen(props){
    const [userDetails,setUserDetails] = useState(blankUser)
    const registerComplete = ()=>{return true;}

    const handle_send = () => {
        console.log("RegisterScreen::handle_send ~ user is: "+ JSON.stringify(userDetails))
        if(isValidUserData(userDetails)){
            var register_request = {...userDetails}
            register_request.type = "register"
            register_request.workflow = props.flowID
            props.webSocket.send(JSON.stringify(register_request))
            if(registerComplete())
                props.update_user_details(userDetails)
        }
    }
    const set_value = (e) =>{
        const value = e.target.value;   
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
      <Input name ="age" placeholder="Age" onChange={set_value} inputProps={ariaLabel} />
      <Input name="id" placeholder="ID" onChange={set_value} inputProps={ariaLabel} />
      <Button onClick={handle_send}>Register</Button>
    </Box></>)
}


export default RegisterScreen;