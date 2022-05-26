import '../App.css';
import { motion } from "framer-motion";

const text = {
    init: { scale: 1 },
    hover1: { scale: 1.2 },
    pressed: { scale: 0.95 }

}

function App() {
    return (
        <>
            <div className="App" >
                <header className="App-header">
                    <div
                        style={{
                            display: "inline-block",
                            height: "auto",
                            width: "auto",
                            backgroundColor: "rgba(225, 225, 255, 0.17)",
                            borderRadius: "0.7em",
                            padding: "4em 6em 3em 6em",
                            backdropFilter: "blur(6px)",

                            // boxShadow: "rgba(100, 100, 111, 0.2) 0px 7px 29px 0px"

                            boxShadow: "rgba(0, 0, 0, 0.25) 0px 14px 28px, rgba(0, 0, 0, 0.22) 0px 10px 10px"
                        }}
                    >
                        <div>
                            <p
                                style={{
                                    letterSpacing: "0.2em",
                                    marginBottom: "2em",
                                }}
                            >COVID-19 MODELS</p>
                            <motion.div
                                className="text"
                                variants={text}
                                whileHover="hover1"
                                whileTap="pressed"
                                style={{
                                    cursor: "pointer"
                                }}
                            >
                                <a href="interface">
                                    <p style={{
                                        letterSpacing: "0.1em",
                                        color: "white",
                                    }}>
                                        开始使用
                                    </p>

                                </a>
                            </motion.div>
                        </div>
                    </div>
                </header>
            </div>
        </>


    )
}

export default App
