import React, { useEffect, useState } from "react"
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';

export default function TestEntryData(props){

    const test_data = props.test_data_entry.test
    const patient = props.test_data_entry.patient
    const [answer,setAnswer] = useState("")
    // useEffect (()=>console.log(answers),[answers]) // for checking purposes only
    // const client = new W3CWebSocket('ws://127.0.0.1:7890');

    const handleClick = ()=>{
    props.send({
        "type":"add results",
        "test":test_data["name"],
        "id":patient,
        "result":answer})
    }
    const onChange = (e)=>{
        setAnswer(e.target.value)
    }
    return (<div>
<Stack>
        
        <div>
          <span>  Name:{test_data.name} <br/>
            Insturction:{test_data.instruction} <br/>
            <TextField id="outlined-basic" label="Outlined" variant="outlined"  onChange={onChange}/><br/><br/>
        </span>
            </div>
        

            </Stack>

            <Button variant="contained" onClick={handleClick}>Submit</Button>
    </div>)
}

