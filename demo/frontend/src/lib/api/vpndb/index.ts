import { supabase } from "./config";

export const detectBlackList = async (ip: string) => {
  const { data } = await supabase.from("blacklist").select("*").eq("ip", ip);

  if (data && data.length > 0) {
    return true;
  }

  return false;
};
