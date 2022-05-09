import React from 'react'
import Button from '@mui/material/Button';


export default function UserNotification (props){

    return(<div>
        {props.notification}
        <Button onClick={props.dismiss}>Dismiss</Button>
    </div>)
} 