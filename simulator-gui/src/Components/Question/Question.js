import { useEffect, useState } from "react"

import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import TextareaAutosize from '@mui/material/TextareaAutosize';

import Stack from '@mui/material/Stack';
import {questionnaire_1} from '../../Mock/MockQuestions'
import Button from '@mui/material/Button';
import { isValidAnswersSet } from "../../Utils/Validations";
export const empty_singlechoice_answer = "No Answer"
// props :{"questions":[{
        //     "text": "Gender",
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

    const [answers,setAnswers] = useState([])

    useEffect(()=>{
      setAnswers(Array.apply(null, Array(props["questionnaire"]["questions"].length)).map(function (x, i) { return ""; }));
      // props["questionnaire"]["questions"].map((question)=>  question_init(question))} , [])
    },[])

    // const 
    const handle_send = () => // we will get connection details in props so we can send it
    {
      if(isValidAnswersSet(answers))
      {
    var questionnaire_answers =  {
          "type": "add answers",
         "questionnaire_number": props.questionnaire["questionnaire_number"], 
         "answers":props["questionnaire"]["questions"].map((question,index) =>{ return ({"question":question,"answer":answers[index]})})
      }
      props.send(questionnaire_answers)
    }
      
    }
      

    const question_init = (question) => {
      const type = question["type"];
    
      if (type ==="one choice"){
        var newArr =[...answers]
        newArr.push(["No Answer"])
        setAnswers(prevState => ([...prevState,"one"]))
        // // setAnswers(prevState => ({...prevState, [question_text]:e}))

        
      }
      else if (type ==="multi"){
        var newArr =[...answers]
        newArr.push([])
        setAnswers(newArr)}
      else if (type ==="open")

      setAnswers(prevState => ([...prevState,"open"]))
    }

    const parse_answers = (answers) => {return answers}
    const getElementOfQuestion = (question,index) => {
      const question_text =question["text"];
      const options = question["options"];
      const type = question["type"];
      const key = question["id"];
      const handleChange = e => {
        let newArr = [...answers]
      
        if(type === "one choice")
          newArr[index] =[e]
        else
          newArr[index] = e
        // // setAnswers(prevState => ({...prevState, [question_text]:e}))
        setAnswers(newArr)

    };
      const changedAnswer = handleChange;
    
      if (type ==="one choice"){
        return (<SingleChoice question ={question_text} options = {options} changedAnswer={changedAnswer} key={key}/>)}
      else if (type ==="multi")
        return (<MultiChoice question ={question_text} options = {options} changedAnswer={changedAnswer} key={key}/>)
      if (type ==="open")
        return (<Open question ={question_text} changedAnswer={changedAnswer} key={key}/>)
    }
    return (
    <div>
      <Stack>
    {props.questionnaire.questions.map((question,index)=>  getElementOfQuestion(question,index))}
    </Stack>
    <Button variant="contained" onClick={handle_send}>Send</Button>

    </div>)

}


export function SingleChoice(props){ // props: {changedAnswer : (answer) => setAnswers(answers => ({...answers, "question": answer}))}

    const [answer,setAnswer] = useState(empty_singlechoice_answer)

    useEffect(()=>props.changedAnswer(answer),[answer])

    const handleChange = (event) => {
        setAnswer(event.target.value);
      }
      
    return (
        <FormControl sx={{ m: 1, minWidth: 120 }}>
        <InputLabel id="demo-simple-select-helper-label">{props.question}</InputLabel>
        <Select
          labelId="demo-simple-select-helper-label"
          id="demo-simple-select-helper"
          value={answer}
          label={props.question}
          onChange={handleChange}
        >
        <MenuItem value={empty_singlechoice_answer} key={-1}>
          <em>None</em>
        </MenuItem>
          {props.options.map((option,key)=><MenuItem value={key} key = {key}>{option}</MenuItem>)}
        </Select>
      </FormControl>
    )
}

export function MultiChoice(props){ // props: {changedAnswer : (answer) => setAnswers(answers => ({...answers, "question": answer}))}

  const [answer,setAnswer] = useState([])

  useEffect(()=>{
    props.changedAnswer(answer)
  },[answer])

    const handleChange = (event) => {
      
      const {
        target: { value },
      } = event;
      setAnswer(value);
    };
  return (
      <FormControl sx={{ m: 1, minWidth: 120 }}>
      <InputLabel id="demo-simple-select-helper-label">{props.question}</InputLabel>
      <Select
        labelId="demo-simple-select-helper-label"
        id="demo-simple-select-helper"
        value={typeof answer === 'string' ? answer.split(',') : answer}
        multiple
        label={props.question}
        onChange={handleChange}
      >
        <MenuItem value="None" key={0}>
          <em>None</em>
        </MenuItem>
        {props.options.map((option,key)=><MenuItem value={key} key={key}>{option}</MenuItem>)}
      </Select>
    </FormControl>
  )
}

export function Open(props){ // props: {changedAnswer : (answer) => setAnswers(answers => ({...answers, "question": answer}))}

  const [answer,setAnswer] = useState('')
  
  useEffect(()=>props.changedAnswer(answer),[answer])

  const handleChange = (event) => {
      setAnswer(event.target.value);
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