import React, { useState, useEffect } from 'react';
import WeaponCard from './WeaponCard';

function WeaponGenerator({ token }) {
  const [worldDescription, setWorldDescription] = useState('');
  const [weaponStream, setWeaponStream] = useState('');
  const [weaponData, setWeaponData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedModel, setSelectedModel] = useState('');
  const [modelOptions, setModelOptions] = useState([]);

  // 动态获取模型列表
  useEffect(() => {
    const fetchModels = async () => {
      try {
        const response = await fetch('http://localhost:8000/models', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        const data = await response.json();
        setModelOptions(data);
        if (data && data.length > 0) {
          setSelectedModel(data[0].value);
        }
      } catch (error) {
        console.error("获取模型列表出错:", error);
      }
    };
    fetchModels();
  }, [token]);

  const handleGenerateStream = async () => {
    setLoading(true);
    setWeaponStream('');
    setWeaponData(null);
    try {
      const response = await fetch('http://localhost:8000/generate_weapon_stream', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ world_description: worldDescription, model: selectedModel })
      });
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let done = false;
      let accumulated = ''; // 缓存所有流式数据
      while (!done) {
        const { value, done: doneReading } = await reader.read();
        done = doneReading;
        const chunkValue = decoder.decode(value);
        const cleanChunk = chunkValue.replace(/^data:\s*/, '');
        if (cleanChunk.trim() !== "") {
          accumulated = cleanChunk;
        }
        setWeaponStream(cleanChunk);
      }
      console.log(accumulated);
      setWeaponStream(accumulated);

      // 尝试解析 JSON 数据
      try {
        const parsedData = JSON.parse(accumulated);
        console.log(parsedData);
        setWeaponData(parsedData);
      } catch (jsonError) {
        console.error("JSON 解析错误:", jsonError);
      }
    } catch (error) {
      console.error("流式生成武器出错:", error);
    }
    setLoading(false);
  };

  return (
    <div className="max-w-xl mx-auto">
      <h2 className="text-2xl mb-4">武器生成（流式输出）</h2>
      <textarea
        placeholder="填写游戏世界观描述……"
        value={worldDescription}
        onChange={(e) => setWorldDescription(e.target.value)}
        className="border p-2 w-full mb-4"
        rows="5"
      />
      <div className="mb-4">
        <label htmlFor="modelSelect" className="mr-2">选择模型:</label>
        <select
          id="modelSelect"
          value={selectedModel}
          onChange={(e) => setSelectedModel(e.target.value)}
          className="border p-2"
        >
          {modelOptions.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </div>
      <button 
        onClick={handleGenerateStream} 
        className="bg-green-500 text-white px-4 py-2 rounded mb-4" 
        disabled={loading}
      >
        {loading ? "生成中..." : "生成武器（流式）"}
      </button>
      
      {/* 如果解析出数据，则展示武器卡和操作按钮 */}
      {weaponData ? (
        <div>
          <WeaponCard weapon={weaponData} />
          <div className="mt-4">
            <button className="bg-blue-500 text-white px-4 py-2 rounded mr-2">保存</button>
            <button className="bg-red-500 text-white px-4 py-2 rounded">放弃</button>
          </div>
        </div>
      ) : (
        // 没有解析成功时展示流式输出的文本
        <div className="border p-4 rounded shadow-md bg-gray-100 whitespace-pre-wrap">
          {weaponStream || (loading ? "等待输出..." : "生成的武器信息将显示在这里")}
        </div>
      )}
    </div>
  );
}

export default WeaponGenerator;
