import 'xterm/css/xterm.css'
import chalk from 'chalk'
import { Terminal } from 'xterm'
import { FitAddon } from 'xterm-addon-fit'
import { WebglAddon } from 'xterm-addon-webgl'
import styles from './App.module.css';
import { onMount, onCleanup } from 'solid-js';

function App() {
  let ws;

  onMount(() => {
    const ele = document.querySelector(`.${styles.xtermContainer}`)
    const term = new Terminal({
      disableStdin: true,
      screenReaderMode: true,
      smoothScrollDuration: 0,
      cursorBlink: true,
    });
    const fitter = new FitAddon()
    term.loadAddon(fitter);
    const gl = new WebglAddon();
    gl.onContextLoss(() => {
      gl.dispose();
    });
    term.loadAddon(gl);
    term.open(ele);
    window.addEventListener('resize', () => {
      fitter.fit();
    });
    fitter.fit()
    ws = new WebSocket(`${document.location.origin.replace('http', 'ws')}/api/log`);
    ws.addEventListener('open', () => {
      term.writeln(chalk.green('connected'));
    });
    ws.addEventListener('message', (e) => {
      term.writeln(e.data);
    });
    ws.addEventListener('close', () => {
      term.writeln(chalk.red('connection lose'));
    });
  });

  onCleanup(() => {
    ws?.close();
  });

  return (
    <div class={styles.xtermContainer}>
    </div>
  );
}

export default App;
