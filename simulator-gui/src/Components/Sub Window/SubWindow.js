import React, {useState} from 'react';
import Card from '@mui/material/Card';
import CardHeader from '@mui/material/CardHeader';
import CardContent from '@mui/material/CardContent';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import PersonIcon from '@mui/icons-material/Person';
import Alert from '@mui/material/Alert';
import Snackbar from '@mui/material/Snackbar';
import Stack from '@mui/material/Stack';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import MoreVertIcon from '@mui/icons-material/MoreVert';
import Questionnaire from '../Question/Question';


import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';

export default function SubWindow(props) { // should have connection object
    const [state,setState] = useState(1);
    
    const [currentComponent,setCurrentComponent] = useState(null)
    
    const [itemsQueue,setItemsQueue] = useState([]);
    
    const isNotification = (item) => false
    const addToQueue = (itemToAdd) => {
      if (isNotification(itemToAdd)){
          handleIncomingNotification(itemToAdd)
      }
      else if (currentComponent != null){
          setItemsQueue(prevState =>[ itemToAdd,...prevState])
        }
        else
        {
          // currentComponent = g
        }
    }

    const handleIncomingNotification = (text) =>
    {
      toast(text, {
        position: "top-right",
        autoClose: 5000,
        hideProgressBar: true,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
        containerId: props.id  

        });
    }
    const styles = {
      position: 'relative',
    
    };
    const renderit=[1,2,3,4,5,6,7,8,9]
  return (
    <div>
    <Card sx={{ maxWidth: 345 , minHeight:300, maxHeight:300 }} >
      <CardHeader
        avatar={
          <PersonIcon>
            
          </PersonIcon>
        }
        action={
          <IconButton aria-label="settings" onClick  = {handleIncomingNotification}>
            <MoreVertIcon  /> {/* change it to fynamically */}

          </IconButton>
        }
        title={props.name}
        subheader={props.role}
      />

{/* Same as */}
      <CardContent >
        <div  style={ {scrollBehavior: "smooth", overflowY: "scroll" , maxHeight:210}}>
        {renderit.map((num)=>     <FormControl sx={{ m: 1, minWidth: 120 }}>
        <InputLabel id="demo-simple-select-helper-label">Age</InputLabel>
        <Select
          labelId="demo-simple-select-helper-label"
          id="demo-simple-select-helper"
          // value={answer}
          label={"Age"}
          // onChange={handleChange}
        >
          <MenuItem value="">
            <em>None</em>
          </MenuItem>
          <MenuItem value={2}>2</MenuItem>
          <MenuItem value={2}>2</MenuItem>

          <MenuItem value={2}>2</MenuItem>

          <MenuItem value={2}>2</MenuItem>

          <MenuItem value={2}>2</MenuItem>

        </Select>
      </FormControl>)}
      </div>
        <Typography variant="body2" color="text.secondary">
       
        {/* <Box
      sx={{
        width: 300,
        height: 300,
        backgroundColor: '#bdbdbd',
       
      }}
    />   */}
            <questionnaire />
        </Typography>


      </CardContent>
      <ToastContainer style={styles}
position="top-right"
autoClose={5000}
hideProgressBar={false}
newestOnTop={false}
closeOnClick
rtl={false}
pauseOnFocusLoss
draggable
pauseOnHover
containerId={props.id}
enableMultiContainer
limit ={1}
/>

    </Card>
    </div>
  );
}
