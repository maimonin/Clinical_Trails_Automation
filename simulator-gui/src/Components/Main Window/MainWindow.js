import React, {useEffect,useState}  from 'react';
import AppBar from '@mui/material/AppBar';
import CssBaseline from '@mui/material/CssBaseline';
import Grid from '@mui/material/Grid';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Link from '@mui/material/Link';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import ScienceIcon from '@mui/icons-material/Science';
import { w3cwebsocket as W3CWebSocket } from "websocket";
import {flow_1,flow_2} from '../../Mock/MockFlow'
import UserWindow from '../UserWindow/UserWindow';
import AddIcon from '@mui/icons-material/Add';
import IconButton from '@mui/material/IconButton';
import Input from '@mui/material/Input';
import Button from '@mui/material/Button';
import ReactFileReader from 'react-file-reader';
  
const flow = flow_2


const theme = createTheme();

export default function MainWindow() {
  const [flowSent,setFlowSent] = useState(false)
  const [screens,setScreens] = useState([])
  const [screensNumber,setScreensNumber] = useState(0)
  
const handle_send_flow = ()=>{
  const ws = new W3CWebSocket('ws://127.0.0.1:7890');
  ws.onopen = ()=>{
  ws.send(JSON.stringify(flow))
  console.log("MainWindow::handle_send_flow ~ sent flow to server")
  setFlowSent(true)
  }
}
  const addUser = ()=>
{
  const newScreens= [...screens]
  newScreens.push(screensNumber)
  setScreensNumber(screensNumber+1)
  setScreens(newScreens)
  console.log(screens)
}
const deleteScreen = (delete_id) =>
{
  const newScreens = screens.filter((id) => id !== delete_id);
  setScreens(newScreens)
}
const handleFiles = files => {
  console.log(files)
}

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AppBar position="relative">
        <Toolbar>
          <ScienceIcon sx={{ mr: 2 }} />
          <Typography variant="h6" color="inherit" noWrap>
            Trial
          </Typography>
        </Toolbar>
      </AppBar>
      <main>

        <Container sx={{ py: 8 }} maxWidth="xl">
        {flowSent?
        <IconButton color="primary" aria-label="add" onClick={addUser}>
        <AddIcon/>
        </IconButton>:<div><ReactFileReader handleFiles={handleFiles} fileTypes={[".json"]} multipleFiles={false} >
  <button className='btn'>Upload</button>
</ReactFileReader><Button onClick={handle_send_flow}>Send</Button></div> }
          <Grid container spacing={4}>
            {
              flowSent?
              screens.map((screen_id) => (
              <Grid item key={screen_id} xs={12} sm={6} md={4}>
                {/* <MemberScreen id={user} user={user}> </MemberScreen> */}
                <UserWindow workflow_id={flow.id} id={screen_id} delete={deleteScreen}> </UserWindow>
              </Grid>
            )) :<div></div>
          }
          </Grid>
        </Container>
      </main>
      {/* Footer */}
      {/* <Box sx={{ bgcolor: 'background.paper', p: 6 }} component="footer">
        <Typography variant="h6" align="center" gutterBottom>
          Footer
        </Typography>
        <Typography
          variant="subtitle1"
          align="center"
          color="text.secondary"
          component="p"
        >
          Something here to give the footer a purpose!
        </Typography>
        <Copyright />
      </Box> */}
      {/* End footer */}
    </ThemeProvider>
  );
}
