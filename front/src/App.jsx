import Interface from "./pages/Interface";
import Home from "./pages/Home";

import {
    BrowserRouter as Router,
    Route,
    Routes
} from "react-router-dom";

function App() {
    return (
        <Router>
            <Routes>
                <Route exact path="/" element={<Home />} />
                <Route exact path="/interface" element={<Interface />} />
            </Routes>
        </Router>
    )
}

export default App
