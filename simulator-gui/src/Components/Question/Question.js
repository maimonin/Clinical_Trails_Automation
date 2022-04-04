import { useEffect, useState } from "react"

import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import TextareaAutosize from '@mui/material/TextareaAutosize';

import Stack from '@mui/material/Stack';
import {questionnaire_1} from '../../Mock/MockQuestions'
import Button from '@mui/material/Button';

// props :{"questions":[{
        //     "Question Text": "Gender",
        //     "type": "onechoice",
        //     "Options": ["Male", "Famale"]
        // },
        // {
        //     "Question Text": "Smoker",
        //     "type": "onechoice",
        //     "Options": ["Yes", "No"]
        // },
        // {
        //     "Question Text": "Pregnant",
        //     "type": "onechoice",
        //     "Options": ["Yes", "No"]
        // },
        // {
        //     "Question Text": "Age",
        //     "type": "open"
        // },
        // {
        //     "Question Text": "Choose each condition that you have been told you have (or had)",
        //     "type": "multichoice",
        //     "Options": ["Cancer", "Diabetes", "Kidney Disease", "Liver Disease", "Stroke", "High Blood Pressure", "Heart Disease", "Angina/Chest Pain", "Ulcers", "Fibromyalgia", "Osteoporosis", "Osteoarthritis", "Rheumatoid", "Arthritis", "Sexually Transmitted Disease", "Allergies/Asthma", "Lung Disease"]
        // }]}
export default function Questionnaire(props){ 
    const [answers,setAnswers] = useState({})
    useEffect(()=>{props.questions.map((question)=>  question_init(question))} , [])
    // const 
    const handle_send = () => // we will get connection details in props so we can send it
    {
      console.log(JSON.stringify(answers))
      // props.connection.send(JSON.stringify(parse_answers(answers)))
    }

    const question_init = (question) => {
      const question_text = question["Question Text"];
      const options = question["Options"];
      const type = question["type"];
    
      if (type ==="onechoice" || type ==="multichoice"){
        setAnswers(prevState => ({...prevState,[question_text]:options[0]}))}
      else // (type ==="open")
        setAnswers(prevState => ({...prevState,[question_text]:""}))}

    const parse_answers = (answers) => {return answers}
    const getElementOfQuestion = (question) => {
      const question_text = question["Question Text"];
      const options = question["Options"];
      const type = question["type"];
      const key = question["id"];
      const handleChange = e => {
        setAnswers(prevState => ({...prevState, [question_text]:e}))

    };
      const changedAnswer = handleChange;
    
      if (type ==="onechoice"){
        return (<SingleChoice question ={question_text} value={answers[question_text]} options = {options} changedAnswer={changedAnswer} key={key}/>)}
      else if (type ==="multichoice")
        return (<MultiChoice question ={question_text} options = {options} changedAnswer={changedAnswer} key={key}/>)
      if (type ==="open")
        return (<Open question ={question_text} changedAnswer={changedAnswer} key={key}/>)
    }
    return (
    <div>
      <Stack>
    {props.questions.map((question)=>  getElementOfQuestion(question))}
    </Stack>
    <Button variant="contained" onClick={handle_send}>Send</Button>

    </div>)

}


export function SingleChoice(props){ // props: {changedAnswer : (answer) => setAnswers(answers => ({...answers, "question": answer}))}

    const [answer,setAnswer] = useState('')
    const handleChange = (event) => {
        console.log("SingleChoice:: change is " + event.target.value + "answer is "+ answer  )

        props.changedAnswer(answer)
        setAnswer(event.target.value);

      }
    return (
        <FormControl sx={{ m: 1, minWidth: 120 }}>
        <InputLabel id="demo-simple-select-helper-label">{props.question}</InputLabel>
        <Select
          labelId="demo-simple-select-helper-label"
          id="demo-simple-select-helper"
          value={props.value}
          label={props.question}
          onChange={handleChange}
        >
         
          {props.options.map((option,key)=><MenuItem value={option} key = {key}>{option}</MenuItem>)}
        </Select>
      </FormControl>
    )
}

export function MultiChoice(props){ // props: {changedAnswer : (answer) => setAnswers(answers => ({...answers, "question": answer}))}

  const [answer,setAnswer] = useState([])

    const handleChange = (event) => {
      
      const {
        target: { value },
      } = event;
      setAnswer(
        // On autofill we get a stringified value.
        typeof value === 'string' ? value.split(',') : value,
      );
      setAnswer(value)
      console.log("value is " + JSON.stringify(value) + ", answer is " + answer)
      props.changedAnswer(answer)
    };
  return (
      <FormControl sx={{ m: 1, minWidth: 120 }}>
      <InputLabel id="demo-simple-select-helper-label">{props.question}</InputLabel>
      <Select
        labelId="demo-simple-select-helper-label"
        id="demo-simple-select-helper"
        value={answer}
        multiple
        label={props.question}
        onChange={handleChange}
      >
        <MenuItem value="" key={0}>
          <em>None</em>
        </MenuItem>
        {props.options.map((option,key)=><MenuItem value={option} key={key}>{option}</MenuItem>)}
      </Select>
    </FormControl>
  )
}

export function Open(props){ // props: {changedAnswer : (answer) => setAnswers(answers => ({...answers, "question": answer}))}

  const [answer,setAnswer] = useState('')
  const handleChange = (event) => {
      setAnswer(event.target.value);
      props.changedAnswer(answer)
    }
  return (
    <div>
  <TextareaAutosize
      maxRows={4}
      aria-label="maximum height"
      placeholder={props.question}
      defaultValue=""
      style={{ width: 275, fontSize: 20 }}
      onChange = {handleChange}
    />
    </div>
  )
}
export function TestQuestionnaire(props){
  return (
    <div>
      <Questionnaire questions = {questionnaire_1["questions"]}/>

  </div>
  )


    }