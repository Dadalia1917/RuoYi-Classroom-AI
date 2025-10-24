package com.ruoyi.web.controller.classroom;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.core.toolkit.Wrappers;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.common.utils.StringUtils;
import com.ruoyi.system.domain.VideoRecords;
import com.ruoyi.system.mapper.VideoRecordsMapper;
import org.springframework.web.bind.annotation.*;

import jakarta.annotation.Resource;

/**
 * 视频检测记录控制器
 * 
 * @author ruoyi
 */
@RestController
@RequestMapping("/videoRecords")
public class VideoRecordsController {
    
    @Resource
    private VideoRecordsMapper videoRecordsMapper;

    /**
     * 获取所有记录
     */
    @GetMapping("/all")
    public AjaxResult GetAll() {
        return AjaxResult.success(videoRecordsMapper.selectList(null));
    }

    /**
     * 根据ID获取记录
     */
    @GetMapping("/{id}")
    public AjaxResult getById(@PathVariable int id) {
        return AjaxResult.success(videoRecordsMapper.selectById(id));
    }

    /**
     * 分页查询
     */
    @GetMapping
    public AjaxResult findPage(@RequestParam(defaultValue = "1") Integer pageNum,
                              @RequestParam(defaultValue = "10") Integer pageSize,
                              @RequestParam(defaultValue = "") String search,
                              @RequestParam(defaultValue = "") String search1,
                              @RequestParam(defaultValue = "") String search3,
                              @RequestParam(defaultValue = "") String search2) {
        LambdaQueryWrapper<VideoRecords> wrapper = Wrappers.<VideoRecords>lambdaQuery();
        wrapper.orderByDesc(VideoRecords::getStartTime);
        if (StringUtils.isNotBlank(search)) {
            wrapper.like(VideoRecords::getUsername, search);
        }
        if (StringUtils.isNotBlank(search1)) {
            wrapper.like(VideoRecords::getStartTime, search1);
        }
        if (StringUtils.isNotBlank(search2)) {
            wrapper.like(VideoRecords::getWeight, search2);
        }
        if (StringUtils.isNotBlank(search3)) {
            wrapper.like(VideoRecords::getConf, search3);
        }
        Page<VideoRecords> page = videoRecordsMapper.selectPage(new Page<>(pageNum, pageSize), wrapper);
        return AjaxResult.success(page);
    }

    /**
     * 删除记录（支持单个和批量删除）
     */
    @DeleteMapping("/delete/{ids}")
    public AjaxResult delete(@PathVariable String ids) {
        if (ids.contains(",")) {
            // 批量删除
            String[] idArray = ids.split(",");
            for (String id : idArray) {
                videoRecordsMapper.deleteById(Integer.parseInt(id.trim()));
            }
        } else {
            // 单个删除
            videoRecordsMapper.deleteById(Integer.parseInt(ids));
        }
        return AjaxResult.success();
    }

    /**
     * 更新记录
     */
    @PutMapping("/updates")
    public AjaxResult updates(@RequestBody VideoRecords videoRecords) {
        videoRecordsMapper.updateById(videoRecords);
        return AjaxResult.success();
    }

    /**
     * 保存记录
     */
    @PostMapping("/save")
    public AjaxResult save(@RequestBody VideoRecords videoRecords) {
        videoRecordsMapper.insert(videoRecords);
        return AjaxResult.success();
    }
}

