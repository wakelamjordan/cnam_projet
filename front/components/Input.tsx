import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { faSistrix } from "@fortawesome/free-brands-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

export function InputWithButton() {
  return (
    <div className="flex w-full max-w-sm items-center space-x-2">
      <Input type="text" placeholder="search" />
      <Button type="submit"><FontAwesomeIcon icon={faSistrix}/></Button>
    </div>
  );
}
