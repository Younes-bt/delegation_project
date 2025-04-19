import { useTranslation } from "react-i18next";

const Home = () => {
  const { t } = useTranslation();
  return (
    <div className="p-10 text-gray-800 dark:text-gray-200 bg-gray-100 dark:bg-gray-800 min-h-screen">
      <h1 className="text-3xl font-bold mb-4">{t("welcome")}</h1>
      <p>{t("description")}</p>
    </div>
  );
};

export default Home;

  