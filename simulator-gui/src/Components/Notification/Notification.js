import React, { useEffect, useState } from "react"
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';

export default function Notification(props){
    const handle_send = () => // we will get connection details in props so we can send it
    {
      console.log(JSON.stringify({action:"dismiss","notification":props.notification}))
      // props.connection.send(JSON.stringify({action:dismiss}))
    }
    return (
    <div>
      <Stack>{JSON.stringify(props.notification)}</Stack>
        <Button variant="contained" onClick={handle_send}>Dismiss</Button>

    </div>)
}

export  function TestNotification(props){
  return (<div><Notification notification="Some Notification"/></div>)
}