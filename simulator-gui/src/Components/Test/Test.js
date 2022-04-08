import React, { useEffect, useState } from "react"
import {tests_1} from "../../Mock/MockTests"
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';

export default function Test(props){


    const [answers,setAnswers] = useState({})
    // useEffect (()=>console.log(answers),[answers]) // for checking purposes only
    useEffect(()=>props.tests.tests.map((test)=>initAnswer(test)),[])
    const initAnswer = (test) =>{
        setAnswers(prev => ({...prev,[test.name]:""}))
    }
    const handleClick = ()=>{
        console.log(answers)
        // props.send(answers)
    }
    const onChange = (e)=>{
        setAnswers(prev => ({...prev,[e.target.name]:e.target.value}))
    }
    return (<div>
<Stack>
        {props.tests.tests.map((test,index)=>
        <div key={index}>
          <span>  Name:{test.name} <br/>
            Insturction:{test.instruction} <br/>
            Facility:{test.Facility} <br/>
            Duration:{test.Duration} <br/> 
            <TextField id="outlined-basic" label="Outlined" variant="outlined" name={test.name} onChange={onChange}/><br/><br/>
        </span>
            </div>
        )}

            </Stack>

            <Button variant="contained" onClick={handleClick}>Submit</Button>
    </div>)
}

export function TestTest(props){

    return (<Test tests={tests_1}/>)
}