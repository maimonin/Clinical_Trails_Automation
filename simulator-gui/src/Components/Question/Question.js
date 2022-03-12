import { useState } from "react"

import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';

export default function Questionnaire(props){
    const [currentQuestion,setCurrentQuestion] = useState(0)
    // const 
    const handle_send = () =>
    {

    }
    
    return (<div>{props.text}</div>)

}


export function SingleChoice(props){
    const [answer,setAnswer] = useState('')
    const handleChange = (event) => {
        setAnswer(event.target.value);
      }
    return (
        <FormControl sx={{ m: 1, minWidth: 120 }}>
        <InputLabel id="demo-simple-select-helper-label">Age</InputLabel>
        <Select
          labelId="demo-simple-select-helper-label"
          id="demo-simple-select-helper"
          value={answer}
          label={props["Question Text"]}
          onChange={handleChange}
        >
          <MenuItem value="">
            <em>None</em>
          </MenuItem>
          {props.Options.map((option)=><MenuItem value={option}>{option}</MenuItem>)}
        </Select>
      </FormControl>
    )
}