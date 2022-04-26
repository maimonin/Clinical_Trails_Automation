import React, { useEffect, useState } from "react"
import {test_data_entry_1} from "../../Mock/MockTests"
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import { w3cwebsocket as W3CWebSocket } from "websocket";

export default function TestEntryData(props){

    const test_data = props.test_data_entry.test
    const patient = props.test_data_entry.patient
    const [answer,setAnswer] = useState("")
    // useEffect (()=>console.log(answers),[answers]) // for checking purposes only
    // const client = new W3CWebSocket('ws://127.0.0.1:7890');

    const handleClick = ()=>{
        // console.log(JSON.stringify(client))
    //    console.log({"type":"add results","id": patient, "test":test_data.name , "result":answer})

        // props.send(answers)
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

export function MockTestDataEntry(props){

    return (<TestEntryData test_data_entry={test_data_entry_1}/>)
}