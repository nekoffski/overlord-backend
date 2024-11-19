import MainGrid from "./MainGrid";
import LogsView from "./LogsView";

export default function MainContent(props) {
  if (props.menuIndex == 0) {
    return <MainGrid />;
  } else if (props.menuIndex == 2) {
    return <LogsView />;
  }
  return <h1>Not implemented</h1>;
}
